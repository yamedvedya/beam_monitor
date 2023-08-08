# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------
import sys

import inspect
import time
import logging
import os
import configparser
import shutil
import numpy as np
from pathlib import Path
from distutils.util import strtobool

import tango
from PyQt5 import QtWidgets, QtCore
from beamline_monitor.gui.mainwindow_ui import Ui_Beam_Monitor
from beamline_monitor.condition_widget import Condition
from beamline_monitor.settings import Settings
from beamline_monitor.alarm_player import PlayAlarm
from beamline_monitor.utils import check_settings
from beamline_monitor import APP_NAME
logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class BeamlineMonitor(QtWidgets.QMainWindow):

    # ----------------------------------------------------------------------
    def __init__(self, options):
        """
        """
        super(BeamlineMonitor, self).__init__()

        # GUI
        self._ui = Ui_Beam_Monitor()
        self._ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.settings = configparser.ConfigParser()

        self.force_close = False

        home = os.path.join(str(Path.home()), '.beamline_monitor')
        if not os.path.exists(home):
            logger.debug(f'Making home folder {home}')
            os.mkdir(home)

        file_name = os.path.join(home, 'settings.ini')

        if not os.path.exists(file_name):
            logger.debug(f'Copying default settings')
            shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default_settings.ini'), file_name)
            check_settings()

        logger.debug(f'Reading settings from {file_name}')
        self.settings.read(file_name)

        if not os.path.exists(os.path.join(home, 'conditions.py')):
            logger.debug(f'Copying default conditions')
            shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conditions_sample.py'),
                        os.path.join(home, 'conditions.py'))

        self.conditions = {}
        self.parse_conditions()

        sys.path.append(home)
        import conditions as conditions_list
        user_conditions_names = [cls_name for cls_name, cls_obj in inspect.getmembers(conditions_list) if
                                       inspect.isclass(cls_obj)]

        self.user_conditions = {}
        for name in user_conditions_names:
            cls = getattr(conditions_list, name)
            try:
                getattr(cls, 'get_state')
                self.user_conditions[name] = cls()
            except AttributeError:
                logger.error(f'Class {name} does not have get_state member')

        self.widgets = {}
        self._ui.layout_conditions.setLayout(QtWidgets.QGridLayout())
        self.setup_gui()

        menubar = self.menuBar()

        self._sound_action = QtWidgets.QAction("Turn off sound", self, triggered=self.mute_sound)
        self._sound_action.setCheckable(True)
        self._sound_action.setEnabled(False)
        menubar.addAction(self._sound_action)

        settings_action = QtWidgets.QAction("Settings", self, triggered=self.show_settings)
        menubar.addAction(settings_action)

        self._menu_list = {}
        self._menu_conditions = QtWidgets.QMenu("Enable/disable conditions", self)
        self.setup_conditions_menu()
        menubar.addAction(self._menu_conditions.menuAction())

        close_action = QtWidgets.QAction("Exit", self, triggered=self._quit_me)
        menubar.addAction(close_action)

        self.beam_status = True

        logger.debug('Set tray icon')
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        show_action.triggered.connect(self._show_me)
        quit_action.triggered.connect(self._quit_me)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self._iconClicked)

        self._msg_box_showed = False
        self._msg_in_telegram_sent = False

        self.sound_muted = False
        self.last_sound_time = time.time()

        self.statusBarLabel = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.statusBarLabel)

        self._refresh_timer = QtCore.QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_status)
        self.restart_timer()

        if strtobool(self.settings['MAIN']['start_windowless']):
            logger.debug('Started windowless')
            self.hide()
            self.tray_icon.show()
        else:
            self.show()

    # ----------------------------------------------------------------------
    def restart_timer(self):
        self._refresh_timer.stop()
        period = int(self.settings['MAIN']['refresh_time'])
        logger.debug(f'Starting condition refresh timer with {period} period')
        self._refresh_timer.start(period)

    # ----------------------------------------------------------------------
    def setup_conditions_menu(self):

        for name, action in self._menu_list.items():
            logger.debug(f'Removing {name} condition from enable menu')
            self._menu_conditions.removeAction(action)

        self._menu_list = {}

        for name in {**self.conditions, **self.user_conditions}.keys():
            logger.debug(f'Adding {name} condition to enable menu')
            self._menu_list[name] = QtWidgets.QAction('{}'.format(name))
            self._menu_list[name].setCheckable(True)
            self._menu_list[name].setChecked(True)
            self._menu_conditions.addAction(self._menu_list[name])

    # ----------------------------------------------------------------------
    def show_settings(self):
        dlg = Settings(self.settings)
        if dlg.exec_():
            logger.debug('Got new settings')
            self.settings = dlg.settings

            with open(os.path.join(os.path.join(str(Path.home()), '.beamline_monitor/'), 'settings.ini'), 'w') as f:
                self.settings.write(f)

            self.parse_conditions()
            self.setup_conditions_menu()
            self.setup_gui()
            self.restart_timer()

    # ----------------------------------------------------------------------
    def parse_conditions(self):
        self.conditions = {}
        for condition in self.settings['CONDITIONS'].values():
            logger.debug(f'New condition: {condition}')
            name, tango_device, attribute, condition, threshold, thr_type = condition.split(';')
            self.conditions[name] = AbstractCondition(tango_device, attribute, condition, threshold, thr_type)

    # ----------------------------------------------------------------------
    def get_sound(self):
        sound = self.settings['ALARM']['sound']
        if sound in ['fire', 'siren', 'rooster']:
            sound = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources'), f"{sound}.mp3")

        logger.debug(f'Alarm sound file: {sound}')
        return sound

    # ----------------------------------------------------------------------
    def setup_gui(self):
        logger.debug(f'Setup GUI')
        layout = self._ui.layout_conditions.layout()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item:
                w = layout.itemAt(i).widget()
                if w:
                    layout.removeWidget(w)
                    w.setVisible(False)

        self.widgets = {}
        counter = 0
        row = 0
        for name in {**self.conditions, **self.user_conditions}:
            self.widgets[name] = Condition(name)
            layout.addWidget(self.widgets[name], row, counter)
            counter += 1
            if counter == int(self.settings['WIDGETS']['widgets_per_row']):
                counter = 0
                row += 1
        logger.debug(f'Setup GUI done')

    # ----------------------------------------------------------------------
    def _refresh_status(self):

        self.beam_status = True
        fault_devices = []

        for name, condition in {**self.conditions, **self.user_conditions}.items():
            status, ui_text = condition.get_state()
            self.widgets[name].ui.lb_State.setText(ui_text)
            if status is None:
                self.widgets[name].ui.lb_State.setStyleSheet('color: orange')
            elif status:
                self.widgets[name].ui.lb_State.setStyleSheet('color: green')
            else:
                self.widgets[name].ui.lb_State.setStyleSheet('color: red')
                if self._menu_list[name].isChecked():
                    self.beam_status *= 0
                    fault_devices.append(name)

        if not self.beam_status:
            logger.debug(f'Beam is not OK!')
            self.show()
            self._ui.lbStatus.setText("not OK")
            self._ui.lbStatus.setStyleSheet('color: red')

            if strtobool(self.settings['MAIN']['show_msgbox']) and not self._msg_box_showed:
                msg = "Problems with: "
                msg += ', '.join(fault_devices)
                logger.debug(f'Show MsgBox')
                self._msg_box_showed = True

                QtWidgets.QMessageBox.warning(self, "Beam problem", msg, QtWidgets.QMessageBox.Ok)
            else:
                logger.debug(f"MsgBox is not shown: main setting: {strtobool(self.settings['MAIN']['show_msgbox'])}" +
                             f", msg_box shown: {self._msg_box_showed}")

            if strtobool(self.settings['TELEGRAMBOT']['enabled']) and not self._msg_in_telegram_sent:
                msg = "Beamline monitor: Beam is not OK\nProblems with: \n"
                msg += '\n'.join(fault_devices)

                if self.settings['TELEGRAMBOT']['specific_server'] != "":
                    server = self.settings['TELEGRAMBOT']['specific_server']
                else:
                    server = self.settings['TELEGRAMBOT']['host'] + ":10000/" + self.settings['TELEGRAMBOT']['server']
                try:
                    tango.DeviceProxy(server).SendMsg(msg)
                    logger.debug(f'Send msg to telegram bot {server}')
                except Exception as err:
                    logger.error(f'Cannot send msg to telegram bot {server}: {err}', exc_info=sys.exc_info())

                self._msg_in_telegram_sent = True

            if not self.sound_muted and not strtobool(self.settings['MAIN']['no_alarm']):
                if time.time() > self.last_sound_time + float(self.settings['ALARM']['repetition_time']):
                    self.last_sound_time = time.time()
                    self._sound_action.setText('Turn off sound')
                    self._sound_action.setEnabled(True)
                    PlayAlarm(self.get_sound()).start()
                else:
                    logger.debug(f"Sound skipped")

        else:
            self._msg_box_showed = False
            self._msg_in_telegram_sent = False
            self.sound_muted = False

            self._sound_action.setEnabled(False)
            self._ui.lbStatus.setText('OK')
            self._ui.lbStatus.setStyleSheet('color: green')

        self.statusBarLabel.setText("Sound: OFF"
                                    if strtobool(self.settings['MAIN']['no_alarm']) or self.sound_muted else
                                    "Sound: ON")

    # ----------------------------------------------------------------------
    def mute_sound(self):
        self.sound_muted = not self.sound_muted
        logger.debug(f'Sound muted: {self.sound_muted}')
        if self.sound_muted:
            self._sound_action.setText('Turn on sound')
        else:
            self._sound_action.setText('Turn off sound')

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        logger.debug(f'Got close event')
        if self.force_close:
            logger.debug(f'Force exit')
            self.tray_icon.hide()
            del self.tray_icon
            event.accept()
        else:
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setText("Would you like to exit (stop monitoring) or minimize it to tray (monitoring will be continued)?")
            msg_box.setWindowTitle("Attention!")
            but = QtWidgets.QPushButton('Close')
            msg_box.addButton(but, QtWidgets.QMessageBox.YesRole)
            msg_box.addButton(QtWidgets.QPushButton('Minimize to tray'), QtWidgets.QMessageBox.NoRole)
            msg_box.setDefaultButton(but)

            ret = msg_box.exec_()
            if ret == 1:
                logger.debug(f'Hide monitor')
                self.hide()
                self.tray_icon.show()
                event.setAccepted(True)
                event.ignore()
            else:
                logger.debug(f'Exit')
                self.tray_icon.hide()
                del self.tray_icon
                event.accept()

    # ----------------------------------------------------------------------
    def _iconClicked(self, reason):
        logger.debug(f'Tray icon clicked: {reason}')
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self._show_me()
        elif reason == QtWidgets.QSystemTrayIcon.Trigger:
            if self.beam_status:
                text = 'OK'
            else:
                text = 'Not OK'
            self.tray_icon.showMessage("Beamline monitor",
                                        "Beam status: {}".format(text),
                                        QtWidgets.QSystemTrayIcon.Information,
                                        2000)

    # ----------------------------------------------------------------------
    def _show_me(self):
        self.show()

    # ----------------------------------------------------------------------
    def _quit_me(self):
        self.force_close = True
        self.close()


# ----------------------------------------------------------------------
class AbstractCondition:

    # ----------------------------------------------------------------------
    def __init__(self, tango_device, attribute, condition, threshold, thr_type):
        self.tango_device = tango_device
        self.attribute = attribute
        self.condition = condition
        self.thr_type = thr_type
        if thr_type == 'float':
            self.threshold = float(threshold)
        elif thr_type == 'int':
            self.threshold = int(threshold)
        else:
            self.threshold = threshold

    # ----------------------------------------------------------------------
    def get_state(self):
        try:
            dev = tango.DeviceProxy(self.tango_device)
            val = getattr(dev, self.attribute)
            attr_conf = dev.get_attribute_config(self.attribute)
            fr = attr_conf.format.strip('%')
            ui_text = f"{val:{fr}}" + attr_conf.unit
            if self.condition == 'more':
                return val > self.threshold, ui_text
            elif self.condition == 'more':
                return val < self.threshold, ui_text
            else:
                if self.thr_type == 'float':
                    return np.isclose(val, self.threshold, rtol=1e-2), ui_text

                return val == self.threshold, ui_text

        except Exception as err:
            logger.error(f'Cannot evaluate {self.attribute} from {self.tango_device} : {repr(err)}')
            return None, ''

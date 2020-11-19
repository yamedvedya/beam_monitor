# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------


import inspect
from distutils.util import strtobool
import time
import conditions as conditions_list
import playsound as psound

from src.server import Info_Server
from settings import *

from PyQt5 import QtWidgets, QtCore
from gui.mainwindow_ui import Ui_Beam_Monitor
from src.condition_widget import Condition

from threading import Thread

# ----------------------------------------------------------------------
class MainRoutine(QtWidgets.QMainWindow):

    # ----------------------------------------------------------------------
    def __init__(self, options):
        """
        """
        super(MainRoutine, self).__init__()

        # GUI
        self._ui = Ui_Beam_Monitor()
        self._ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self._get_conditions()
        self._setupGui()
        self._setupMenu()

        self.beam_status = True

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        show_action.triggered.connect(self._showMe)
        quit_action.triggered.connect(self._quitMe)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self._iconClicked)

        if strtobool(options.notify):
            from notify_run import Notify
            self._notify = True
            self.notifyChannel = Notify('https://notify.run/api/', 'https://notify.run/ocnh6HqhiGAAnQQl')
            self.backNotificationSent = False
            self.lostNotificationSent = False
        else:
            self._notify = False

        self._show_msg_box = strtobool(options.msgbox)
        self._msg_box_showed = False

        self.sound_on = self.sound_triggered = strtobool(options.alarm)
        if self.sound_on:
            self.lastSoundTime = time.time()
            self.sound = options.sound

        self.statusBarLabel = QtWidgets.QLabel("Sound: {}".format(str(self.sound_on)))
        self.statusBar().addPermanentWidget(self.statusBarLabel)
        self._refreshTimer = QtCore.QTimer(self)
        self._refreshTimer.timeout.connect(self._refreshStatus)
        self._refreshTimer.start(500)

        self.exitOnClose = False

        self._server = Info_Server('', int(options.port), self)

        if strtobool(options.windowless):
            self.hide()
            self.tray_icon.show()

    # ----------------------------------------------------------------------
    def _get_conditions(self):
        self._conditions_names = [cls_name for cls_name, cls_obj in inspect.getmembers(conditions_list) if
                                  inspect.isclass(cls_obj) and cls_name != 'AbstractCondition']

        self.conditions = {}
        for name in self._conditions_names:
            self.conditions[name] = getattr(conditions_list, name)()

    # ----------------------------------------------------------------------
    def _setupMenu(self):

        self._soundAction = QtWidgets.QAction("Turn off sound", self,
                                               triggered=self._trunOnSound)
        self._soundAction.setCheckable(True)

        self._closeAction = QtWidgets.QAction("Exit", self,
                                          triggered=self._quitMe)

        _menu_components = QtWidgets.QMenu("Values to be monitored", self)
        _setup_menu = QtWidgets.QMenu("Setup thresholds", self)

        self._menu_list = {}
        self._setup_condition = {}

        for name in self._conditions_names:
            self._menu_list[name] = QtWidgets.QAction('{}'.format(name))
            self._menu_list[name].setCheckable(True)
            self._menu_list[name].setChecked(True)
            _menu_components.addAction(self._menu_list[name])

            self._setup_condition[name] = QtWidgets.QAction('{}'.format(name))
            self._setup_condition[name].triggered.connect(self.widgets[name].setup_condition)
            _setup_menu.addAction(self._setup_condition[name])

        menubar = self.menuBar()
        menubar.addAction(self._soundAction)
        self._soundAction.setEnabled(False)
        menubar.addAction(_menu_components.menuAction())
        menubar.addAction(_setup_menu.menuAction())
        menubar.addAction(self._closeAction)

    # ----------------------------------------------------------------------
    def _setupGui(self):

        condition_grid = QtWidgets.QGridLayout(self._ui.layout_conditions)
        layout = condition_grid.layout()
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
        for name in self._conditions_names:
            self.widgets[name] = Condition(name, self.conditions[name])
            layout.addWidget(self.widgets[name], row, counter)
            counter += 1
            if counter == WIDGETS_PER_ROW:
                counter = 0
                row += 1

    # ----------------------------------------------------------------------
    def _sendTest(self):

        self.notifyChannel.send('Test!')

    # ----------------------------------------------------------------------
    def _refreshStatus(self):

        self.beam_status = True
        faulte_devices = []

        for name in self._conditions_names:
            status, ui_text = self.conditions[name].get_state()
            self.widgets[name]._ui.lb_State.setText(ui_text)
            if status == 'not_ok':
                self.widgets[name]._ui.lb_State.setStyleSheet('color: red')
                if self._menu_list[name].isChecked():
                    self.beam_status *= 0
                    faulte_devices.append(name)
            elif status == 'ok':
                self.widgets[name]._ui.lb_State.setStyleSheet('color: green')
            else:
                self.widgets[name]._ui.lb_State.setStyleSheet('color: orange')

        if not self.beam_status:
            self.show()
            self._ui.lbStatus.setText("not OK")
            self._ui.lbStatus.setStyleSheet('color: red')

            if self._show_msg_box and not self._msg_box_showed:
                self._msg_box_showed = False
                msg = "Probles with: "
                msg += ', '.join(faulte_devices)

                QtWidgets.QMessageBox.warning(self, "Beam problem", msg, QtWidgets.QMessageBox.Ok)

            if self.sound_triggered and self.sound_on:
                if time.time() > self.lastSoundTime + SOUNDREPEATTIME:
                    self.lastSoundTime = time.time()
                    self._soundAction.setText('Turn off sound')
                    self._soundAction.setEnabled(True)
                    Thread(target=psound.playsound('./resources/{}.mp3'.format(self.sound), True)).start()

            if self._notify:
                if not self.lostNotificationSent:
                    self.notifyChannel.send('Beam lost')
                    self.backNotificationSent = False
                    self.lostNotificationSent = True
        else:
            self._msg_box_showed = False

            if self.sound_on:
                self.sound_triggered = True

            self._soundAction.setEnabled(False)
            self._ui.lbStatus.setText('OK')
            self._ui.lbStatus.setStyleSheet('color: green')

            if self._notify:
                if not self.backNotificationSent:
                    self.notifyChannel.send('Beam back')
                    self.backNotificationSent = True
                    self.lostNotificationSent = False

        self.statusBarLabel.setText("Sound: {}".format(str(self.sound_on and self.sound_triggered)))

    # ----------------------------------------------------------------------
    def _trunOnSound(self):
        self.sound_triggered = not self.sound_triggered
        if self.sound_triggered:
            self._soundAction.setText('Turn off sound')
        else:
            self._soundAction.setText('Turn on sound')

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        if self.exitOnClose:
            self._server.stop_server()
            self.tray_icon.hide()
            del self.tray_icon
            event.accept()
        else:
            self.hide()
            self.tray_icon.show()
            event.setAccepted(True)
            event.ignore()

    # ----------------------------------------------------------------------
    def _iconClicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self._showMe()
        elif reason == QtWidgets.QSystemTrayIcon.Trigger:
            if self.beam_status:
                text = 'OK'
            else:
                text = 'Not OK'
            self.tray_icon.showMessage("Beam monitor",
                                        "Beam status: {}".format(text),
                                        QtWidgets.QSystemTrayIcon.Information,
                                        2000)

    # ----------------------------------------------------------------------
    def _showMe(self):
        self.show()

    # ----------------------------------------------------------------------
    def _quitMe(self):
        self.exitOnClose = True
        self.close()
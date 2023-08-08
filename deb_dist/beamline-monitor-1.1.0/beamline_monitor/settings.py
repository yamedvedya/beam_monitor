# Created by matveyev at 06.12.2022

import logging

from PyQt5 import QtWidgets, QtCore

from distutils.util import strtobool
from pathlib import Path

from beamline_monitor.gui.setup_ui import Ui_Settings
from beamline_monitor.condition_setup import ConditionSetup
from beamline_monitor.utils import get_server_name_by_class, refresh_combo_box
from beamline_monitor import APP_NAME
logger = logging.getLogger(APP_NAME)


class Settings(QtWidgets.QDialog):
    # ----------------------------------------------------------------------
    def __init__(self, settings):
        super(Settings, self).__init__()

        self._ui = Ui_Settings()
        self._ui.setupUi(self)

        self.settings = settings

        self._ui.chk_msgbox.setChecked(strtobool(self.settings['MAIN']['show_msgbox']))
        self._ui.chk_windowless.setChecked(strtobool(self.settings['MAIN']['start_windowless']))
        self._ui.chk_no_alarm.setChecked(strtobool(self.settings['MAIN']['no_alarm']))

        self._ui.rb_fire.setChecked(self.settings['ALARM']['sound'] == 'fire')
        self._ui.rb_siren.setChecked(self.settings['ALARM']['sound'] == 'siren')
        self._ui.rb_rooster.setChecked(self.settings['ALARM']['sound'] == 'rooster')
        user_file = self.settings['ALARM']['sound'] not in ['fire', 'siren', 'rooster']
        self._ui.rb_user.setChecked(user_file)
        self._ui.le_file.setEnabled(user_file)
        self._ui.cmd_file.setEnabled(user_file)
        if user_file:
            self._ui.le_file.setText(user_file)

        self._ui.sp_widgets_per_row.setValue(int(self.settings['WIDGETS']['widgets_per_row']))

        self._ui.sp_refresh.setValue(int(self.settings['MAIN']['refresh_time']))
        self._ui.dsp_alarm_refresh.setValue(float(self.settings['ALARM']['repetition_time']))

        self._ui.rb_user.toggled.connect(lambda checked: self._ui.le_file.setEnabled(checked))
        self._ui.rb_user.toggled.connect(lambda checked: self._ui.cmd_file.setEnabled(checked))

        self._ui.cmd_file.clicked.connect(self.select_file)
        self._ui.cmd_add_condition.clicked.connect(self.add_condition)

        ind = 0
        for ind, condition in enumerate(self.settings['CONDITIONS'].values()):
            widget = ConditionSetup(ind, condition)
            widget.delete_me.connect(self.delete_condition)
            widget.new_name.connect(self.new_condition_name)
            self._ui.tw_conditions.addTab(widget, widget.my_name())

        self._condition_counter = ind + 1

        try:
            self.restoreGeometry(QtCore.QSettings(APP_NAME).value(f"{APP_NAME}Settings/geometry"))
        except:
            pass

        self._ui.chk_specify_server.clicked.connect(self.set_manual_telegram_server)
        self._ui.le_tango_host.editingFinished.connect(self.change_tango_host)

        telergam_bot = strtobool(self.settings['TELEGRAMBOT']['enabled'])
        self._ui.gr_telegram_bot.setChecked(telergam_bot)
        if telergam_bot:
            if self.settings['TELEGRAMBOT']['specific_server']:
                self._ui.chk_specify_server.setChecked(True)
                self._ui.le_telegram_server.setText(self.settings['TELEGRAMBOT']['specific_server'])
            else:
                self._ui.chk_specify_server.setChecked(False)
                self._ui.le_tango_host.setText(self.settings['TELEGRAMBOT']['host'])
                self.change_tango_host()
                refresh_combo_box(self._ui.cmb_telegram_bot, self.settings['TELEGRAMBOT']['server'])

    # ----------------------------------------------------------------------
    def set_manual_telegram_server(self, state):
        self._ui.le_tango_host.setEnabled(not state)
        self._ui.cmb_telegram_bot.setEnabled(not state)
        self._ui.le_telegram_server.setEnabled(state)

    # ----------------------------------------------------------------------
    def change_tango_host(self):
        self._ui.cmb_telegram_bot.clear()
        self._ui.cmb_telegram_bot.addItems(get_server_name_by_class(self._ui.le_tango_host.text()))

    # ----------------------------------------------------------------------
    def delete_condition(self, index):
        tab_to_delete = None
        for ind in range(self._ui.tw_conditions.count()):
            if self._ui.tw_conditions.widget(ind).my_id() == index:
                tab_to_delete = ind

        if tab_to_delete is not None:
            self._ui.tw_conditions.removeTab(tab_to_delete)

    # ----------------------------------------------------------------------
    def new_condition_name(self, index, new_name):
        for ind in range(self._ui.tw_conditions.count()):
            if self._ui.tw_conditions.widget(ind).my_id() == index:
                self._ui.tw_conditions.setTabText(ind, new_name)

    # ----------------------------------------------------------------------
    def add_condition(self):
        widget = ConditionSetup(self._condition_counter)
        widget.delete_me.connect(self.delete_condition)
        widget.new_name.connect(self.new_condition_name)
        self._ui.tw_conditions.addTab(widget, widget.my_name())

        self._condition_counter += 1

    # ----------------------------------------------------------------------
    def select_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', Path.home(), "Mp3 files (*.mp3)")
        if fname:
            self._ui.le_file.setText(fname)

    # ----------------------------------------------------------------------
    def accept(self):

        self.settings['MAIN']['show_msgbox'] = str(self._ui.chk_msgbox.isChecked())
        self.settings['MAIN']['start_windowless'] = str(self._ui.chk_windowless.isChecked())
        self.settings['MAIN']['no_alarm'] = str(self._ui.chk_no_alarm.isChecked())

        if self._ui.rb_fire.isChecked():
            self.settings['ALARM']['sound'] = 'fire'
        elif self._ui.rb_siren.isChecked():
            self.settings['ALARM']['sound'] = 'siren'
        elif self._ui.rb_rooster.isChecked():
            self.settings['ALARM']['sound'] = 'rooster'
        else:
            self.settings['ALARM']['sound'] = self._ui.le_file.text()

        self.settings['WIDGETS']['widgets_per_row'] = str(self._ui.sp_widgets_per_row.value())

        self.settings['MAIN']['refresh_time'] = str(self._ui.sp_refresh.value())
        self.settings['ALARM']['repetition_time'] = str(self._ui.dsp_alarm_refresh.value())

        self.settings['CONDITIONS'] = {}

        for ind in range(self._ui.tw_conditions.count()):
            self.settings['CONDITIONS'][str(ind)] = self._ui.tw_conditions.widget(ind).get_data()

        telergam_bot = self._ui.gr_telegram_bot.isChecked()
        self.settings['TELEGRAMBOT']['enabled'] = str(telergam_bot)
        if telergam_bot:
            if self._ui.chk_specify_server.isChecked():
                self.settings['TELEGRAMBOT']['specific_server'] = self._ui.le_telegram_server.text()
                self.settings['TELEGRAMBOT']['host'] = ""
                self.settings['TELEGRAMBOT']['server'] = ""
            else:
                self.settings['TELEGRAMBOT']['specific_server'] = ""
                self.settings['TELEGRAMBOT']['host'] = self._ui.le_tango_host.text()
                self.settings['TELEGRAMBOT']['server'] = self._ui.cmb_telegram_bot.currentText()
        else:
            self.settings['TELEGRAMBOT']['specific_server'] = ""
            self.settings['TELEGRAMBOT']['host'] = ""
            self.settings['TELEGRAMBOT']['server'] = ""

        QtCore.QSettings(APP_NAME).setValue(f"{APP_NAME}Settings/geometry", self.saveGeometry())

        super(Settings, self).accept()

    # ----------------------------------------------------------------------
    def reject(self):

        QtCore.QSettings(APP_NAME).setValue(f"{APP_NAME}Settings/geometry", self.saveGeometry())

        super(Settings, self).reject()

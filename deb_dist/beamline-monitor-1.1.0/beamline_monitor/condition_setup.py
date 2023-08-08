# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 06/12/2022
# ----------------------------------------------------------------------

import tango
import re
import numpy as np

from PyQt5 import QtWidgets, QtCore

from beamline_monitor.gui.condition_setup_ui import Ui_ConditionSetup
from beamline_monitor.utils import refresh_combo_box


# ----------------------------------------------------------------------
class ConditionSetup(QtWidgets.QDialog):

    delete_me = QtCore.pyqtSignal(int)
    new_name = QtCore.pyqtSignal(int, str)

    # ----------------------------------------------------------------------
    def __init__(self, my_id, condition=None):

        super(ConditionSetup, self).__init__()

        self._my_type = float
        self._my_id = my_id

        self._ui = Ui_ConditionSetup()
        self._ui.setupUi(self)

        self._ui.le_device.editingFinished.connect(self.refresh_attributes)
        self._ui.cmb_attribute.currentTextChanged.connect(self.new_attribute)
        self._ui.cmd_delete_me.clicked.connect(lambda state, x=my_id: self.delete_me.emit(x))
        self._ui.le_name.textChanged.connect(lambda text, x=my_id: self.new_name.emit(x, text))

        if condition is not None:
            name, tango_device, attribute, condition, threshold, _ = condition.split(';')

            self._ui.le_name.setText(name)
            self._ui.le_device.setText(tango_device)
            self.refresh_attributes()

            refresh_combo_box(self._ui.cmb_attribute, attribute)
            refresh_combo_box(self._ui.cmb_condition, condition)

            if self._my_type == float:
                self._ui.dsp_threshold.setValue(float(threshold))
            elif self._my_type == int:
                self._ui.sp_threshold.setValue(int(threshold))
            else:
                self._ui.le_value.setText(threshold)

    # ----------------------------------------------------------------------
    def my_id(self):
        return self._my_id

    # ----------------------------------------------------------------------
    def my_name(self):
        return self._ui.le_name.text()

    # ----------------------------------------------------------------------
    def get_data(self):
        if self._my_type == float:
            my_type = 'float'
            threshold = str(self._ui.dsp_threshold.value())
        elif self._my_type == int:
            my_type = 'int'
            threshold = str(self._ui.sp_threshold.value())
        else:
            my_type = 'str'
            threshold = self._ui.le_value.text()

        return ';'.join([self._ui.le_name.text(),
                         self._ui.le_device.text(),
                         self._ui.cmb_attribute.currentText(),
                         self._ui.cmb_condition.currentText(),
                         threshold,
                         my_type])

    # ----------------------------------------------------------------------
    def refresh_attributes(self):
        current_attribute = self._ui.cmb_attribute.currentText()
        self._ui.cmb_attribute.blockSignals(True)
        self._ui.cmb_attribute.clear()
        try:
            dev = tango.DeviceProxy(self._ui.le_device.text())
            self._ui.cmb_attribute.addItems(dev.get_attribute_list())
        except:
            pass
        if not refresh_combo_box(self._ui.cmb_attribute, current_attribute):
            self.new_attribute(self._ui.cmb_attribute.currentText())

        self._ui.cmb_attribute.blockSignals(False)

    # ----------------------------------------------------------------------
    def new_attribute(self, attribute):
        self._ui.sp_threshold.setVisible(False)
        self._ui.dsp_threshold.setVisible(False)
        self._ui.le_value.setVisible(False)
        self._ui.cmb_condition.clear()

        try:
            atr = tango.DeviceProxy(self._ui.le_device.text()).get_attribute_config(attribute)
            if atr.data_type in [tango.DevDouble, tango.DevFloat]:
                self._my_type = float
                self._ui.dsp_threshold.setVisible(True)
                self._ui.cmb_condition.addItems(['equal', 'less', 'more'])
                power = re.findall('\d+.\d+', atr.format)
                if power:
                    exp, dec = [int(v) for v in power[0].split('.')]
                else:
                    exp, dec = 8, 4
                self._ui.dsp_threshold.setDecimals(dec)
                self._ui.dsp_threshold.setMaximum(np.power(10, exp))
                self._ui.dsp_threshold.setMinimum(-np.power(10, exp))
            elif atr.data_type in [tango.DevShort, tango.DevUShort, tango.DevLong, tango.DevULong,
                                   tango.DevULong64, tango.DevLong64, tango.DevInt]:

                self._my_type = int
                self._ui.sp_threshold.setVisible(True)
                self._ui.cmb_condition.addItems(['equal', 'less', 'more'])
                power = re.findall('\d+', atr.format)
                if power:
                    exp = int(power[0])
                else:
                    exp = 8
                self._ui.sp_threshold.setMaximum(int(np.power(10, exp)))
                self._ui.sp_threshold.setMinimum(-int(np.power(10, exp)))
            else:
                self._ui.le_value.setVisible(True)
                self._ui.cmb_condition.addItem('equal')
        except:
            pass

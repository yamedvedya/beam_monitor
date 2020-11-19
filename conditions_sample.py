# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------


import PyTango
import numpy as np
from src.abstract_condition import AbstractCondition


class Petra_Current(AbstractCondition):

    # ----------------------------------------------------------------------
    def __init__(self):
        super(Petra_Current, self).__init__()

        self.device_proxy = PyTango.DeviceProxy('hasep23oh:10000/petra/globals/keywords')
        self._threshold = 90
        self._mode = 'More'

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            PCurrent = self.device_proxy.BeamCurrent
            gotPcurrent = True
        except:
            gotPcurrent = False

        if gotPcurrent:
            ui_text = '{} mA'.format(int(PCurrent))
            status = 'ok'
            if self._mode == 'More' and int(PCurrent) < self._threshold:
                status = 'not_ok'
            elif self._mode == 'Less' and int(PCurrent) > self._threshold:
                status = 'not_ok'
            elif self._mode == 'Equal' and int(PCurrent) != self._threshold:
                status = 'not_ok'
        else:
            status = 'nc'
            ui_text = 'NC'

        return status, ui_text

    # ----------------------------------------------------------------------
    def get_threshold(self):

        return self._threshold, self._mode

    # ----------------------------------------------------------------------
    def get_threshold_type(self):

        return 'SpinBox', [0, 120], True

    # ----------------------------------------------------------------------
    def set_threshold(self, value):

        self._threshold = value

    # ----------------------------------------------------------------------
    def set_mode(self, mode):

        self._mode = mode


# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Petra_Bunches(AbstractCondition):

    # ----------------------------------------------------------------------
    def __init__(self):
        super(Petra_Bunches, self).__init__()

        self.device_proxy = PyTango.DeviceProxy('hasep23oh:10000/petra/globals/keywords')
        self.threshold = 480

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            PBunches = self.device_proxy.NumberOfBunches
            gotPbunches = True
        except:
            gotPbunches = False

        if gotPbunches:
            ui_text = '{}'.format(int(PBunches))
            if int(PBunches) == self.threshold:
                status = 'ok'
            else:
                status = 'not_ok'
        else:
            ui_text = 'NC'
            status = 'nc'

        return status, ui_text

    # ----------------------------------------------------------------------
    def get_threshold(self):

        return self.threshold, 'Equal'

    # ----------------------------------------------------------------------
    def get_threshold_type(self):

        return 'ComboBox', ['40', '80', '480'], False

    # ----------------------------------------------------------------------
    def set_threshold(self, value):

        self.threshold = value


# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Beam_Energy(AbstractCondition):

    # ----------------------------------------------------------------------
    def __init__(self):
        super(Beam_Energy, self).__init__()

        self.device_proxy = PyTango.DeviceProxy('hasep23oh:10000/p23/dcmener/oh.01')
        self.threshold = None

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            ui_text = "{:.2f} eV".format(self.device_proxy.position)
        except:
            ui_text = 'OK'

        return 'ok', ui_text
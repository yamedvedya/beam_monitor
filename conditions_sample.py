import PyTango
import numpy as np

# ----------------------------------------------------------------------
# each class has to have function "get_state" which has to return 1) status = "ok", "not_ok" or "nc" and
#                                                                 2) ui_text
# ----------------------------------------------------------------------

class Petra_Current(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('petra/globals/keywords')
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

class Petra_Bunches(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('petra/globals/keywords')
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
    def set_mode(self, mode):

        pass

# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Beam_Energy(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('p23/dcmener/oh.01')
        self.threshold = None

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            ui_text = "{:.2f} eV".format(self.device_proxy.position)
        except:
            ui_text = 'OK'

        return 'ok', ui_text

    # ----------------------------------------------------------------------
    def get_threshold(self):

        return None, None

    # ----------------------------------------------------------------------
    def get_threshold_type(self):

        return 'No', None, False

    # ----------------------------------------------------------------------
    def set_threshold(self, value, condition):

        pass

    # ----------------------------------------------------------------------
    def set_mode(self, mode):

        pass
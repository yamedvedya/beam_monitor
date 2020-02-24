import PyTango
import numpy as np

# ----------------------------------------------------------------------
# each class has to have function "get_state" which has to return 1) status = "ok", "not_ok" or "nc" and
#                                                                 2) ui_text
# ----------------------------------------------------------------------
class LM4(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('hasylab/p22_lm4/output')

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            max_lm4 = self.device_proxy.Frame.max()
        except:
            max_lm4 = False

        if max_lm4:
            if max_lm4 < 50:
                ui_text = 'No beam'
                status = 'not_ok'
            else:
                status = 'ok'
                ui_text = 'OK'
        else:
            status = 'nc'
            ui_text = 'NC'

        return status, ui_text

# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class V2(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/v2')

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            v2State = self.device_proxy.stellung[0]
        except:
            v2State = False

        if v2State:
            if int(v2State) != 2:
                ui_text = "closed"
                status = 'not_ok'
            else:
                ui_text = "open"
                status = 'ok'
        else:
            ui_text = 'NC'
            status = 'nc'

        return status, ui_text
# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class PS2(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/ps2')

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            ps2State = self.device_proxy.stellung[0]
        except:
            ps2State = False

        if ps2State:
            if int(ps2State) != 2:
                ui_text = "closed"
                status = 'not_ok'
            else:
                ui_text = "open"
                status = 'ok'
        else:
            ui_text = 'NC'
            status = 'nc'

        return status, ui_text

# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Petra_Current(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('petra/globals/keywords')

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            PCurrent = self.device_proxy.BeamCurrent
            gotPcurrent = True
        except:
            gotPcurrent = False

        if gotPcurrent:
            ui_text = '{} mA'.format(int(PCurrent))
            if int(PCurrent) < 60:
                status = 'not_ok'
            else:
                status = 'ok'
        else:
            status = 'nc'
            ui_text = 'NC'

        return status, ui_text


# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Petra_Bunches(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('petra/globals/keywords')

    # ----------------------------------------------------------------------
    def get_state(self):

        try:
            PBunches = self.device_proxy.NumberOfBunches
            gotPbunches = True
        except:
            gotPbunches = False

        if gotPbunches:
            ui_text = '{}'.format(int(PBunches))
            if int(PBunches) in [40, 80, 480]:
                status = 'ok'
            else:
                status = 'not_ok'
        else:
            ui_text = 'NC'
            status = 'nc'

        return status, ui_text


# ----------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------

class Beam_Energy(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.device_proxy = PyTango.DeviceProxy('p22/dcmener/oh.01')

    # ----------------------------------------------------------------------
    def get_state(self):


        try:
            ui_text = "{:.2f} eV".format(self.device_proxy.position)
        except:
            ui_text = 'OK'

        return 'ok', ui_text
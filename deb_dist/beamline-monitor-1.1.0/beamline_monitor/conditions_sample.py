"""
Author:   y.matveev@gmail.com
Modified: 26/02/2020

Every user condition should be a class, containing get_state() member,
which returns tuple (condition_state: bool or None, ui_text: str),
where condition_state: True - condition fulfilled, no alarm
                       False - condition not fulfilled, raise alarm
                       None - condition cannot be evaluated 
                       
This is a simple example:

import PyTango


class Petra_Current():

    # ----------------------------------------------------------------------
    @staticmethod
    def get_state():

        try:
            PCurrent = PyTango.DeviceProxy('hasep23oh:10000/petra/globals/keywords').BeamCurrent
            ui_text = '{} mA'.format(int(PCurrent))
            status = int(PCurrent) > 100 
        except:
            status = None
            ui_text = 'NC'

        return status, ui_text
"""
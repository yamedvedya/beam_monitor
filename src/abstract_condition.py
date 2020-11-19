# Created by matveyev at 19.11.2020

class AbstractCondition(object):
    def __init__(self):
        super(AbstractCondition, self).__init__()

    # ----------------------------------------------------------------------
    def get_state(self):
        return 'nc', ''

    # ----------------------------------------------------------------------
    def get_threshold(self):

        return None, None

    # ----------------------------------------------------------------------
    def get_threshold_type(self):

        return 'No', None, False

    # ----------------------------------------------------------------------
    def set_threshold(self, value):

        pass

    # ----------------------------------------------------------------------
    def set_mode(self, mode):

        pass
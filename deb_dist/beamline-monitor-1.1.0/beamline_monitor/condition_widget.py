# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------


from PyQt5 import QtWidgets
from beamline_monitor.gui.condition_ui import Ui_condition


# ----------------------------------------------------------------------
class Condition(QtWidgets.QWidget):

    # ----------------------------------------------------------------------
    def __init__(self, caption):

        super(Condition, self).__init__()

        self.ui = Ui_condition()
        self.ui.setupUi(self)
        self.ui.lb_Caption.setText(caption)
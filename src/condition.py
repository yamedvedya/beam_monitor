# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------


from PyQt5 import QtWidgets
from uis.condition_ui import Ui_condition

# ----------------------------------------------------------------------
class Condition(QtWidgets.QWidget):

    # ----------------------------------------------------------------------
    def __init__(self, caption):

        super(Condition, self).__init__()

        self._ui = Ui_condition()
        self._ui.setupUi(self)
        self._ui.lb_Caption.setText(caption)
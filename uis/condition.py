from PyQt4 import QtGui
from condition_ui import Ui_condition

# ----------------------------------------------------------------------
class Condition(QtGui.QWidget):

    # ----------------------------------------------------------------------
    def __init__(self, caption):

        super(Condition, self).__init__()

        self._ui = Ui_condition()
        self._ui.setupUi(self)
        self._ui.lb_Caption.setText(caption)
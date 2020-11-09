from PyQt5 import QtWidgets, QtCore

from uis.condition_ui import Ui_condition
from src.condition_setup import ConditionSetup


# ----------------------------------------------------------------------
class Condition(QtWidgets.QWidget):

    # ----------------------------------------------------------------------
    def __init__(self, caption, condition_class):

        super(Condition, self).__init__()

        self._ui = Ui_condition()
        self._ui.setupUi(self)
        self._ui.lb_Caption.setText(caption)

        self._setting_window = ConditionSetup(caption, condition_class)
        self.editable = self._setting_window.editable

    # ----------------------------------------------------------------------
    def setup_condition(self):
        self._setting_window.show()
from PyQt5 import QtWidgets, QtCore
from gui.condition_setup_ui import Ui_ConditionSetup


# ----------------------------------------------------------------------
class ConditionSetup(QtWidgets.QDialog):

    # ----------------------------------------------------------------------
    def __init__(self, caption, condition_class):

        super(ConditionSetup, self).__init__()

        self._ui = Ui_ConditionSetup()
        self._ui.setupUi(self)

        self._ui.lb_name.setText(caption)

        self._condition_class = condition_class

        self.ui_type, ui_params, adjustable_condition = self._condition_class.get_threshold_type()
        current_value, current_mode = self._condition_class.get_threshold()

        if self.ui_type.lower() == 'label':
            self.threshold_ui = QtWidgets.QLabel(self)
            self.threshold_ui.setAlignment(QtCore.Qt.AlignCenter)
            self.threshold_ui.setText('{}'.format(current_value))
        elif self.ui_type.lower() == 'spinbox':
            self.threshold_ui = QtWidgets.QSpinBox(self)
            self.threshold_ui.setMinimum(ui_params[0])
            self.threshold_ui.setMaximum(ui_params[1])
            self.threshold_ui.setProperty("value", current_value)
            self.threshold_ui.valueChanged.connect(self._condition_class.set_threshold)
        elif self.ui_type.lower() == 'doublespinbox':
            self.threshold_ui = QtWidgets.QDoubleSpinBox(self)
            self.threshold_ui.setMinimum(ui_params[0])
            self.threshold_ui.setMaximum(ui_params[1])
            self.threshold_ui.setProperty("value", current_value)
            self.threshold_ui.valueChanged.connect(self._condition_class.set_threshold)
        elif self.ui_type.lower() == 'combobox':
            self.threshold_ui = QtWidgets.QComboBox(self)
            self.threshold_ui.addItems(ui_params)
            refresh_combo_box(self.threshold_ui, str(current_value))
            self.threshold_ui.currentTextChanged.connect(lambda text: self._condition_class.set_threshold(text))
        else:
            self.threshold_ui = None

        refresh_combo_box(self._ui.cmb_condition, str(current_mode))
        self._ui.cmb_condition.setEnabled(adjustable_condition)
        self._ui.cmb_condition.currentTextChanged.connect(self._condition_class.set_mode)

        if self.threshold_ui is not None:
            self.threshold_ui.setObjectName("threshold_ui")
            self._ui.horizontalLayout.addWidget(self.threshold_ui)
            self.editable = True
        else:
            self.editable = False

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        self.hide()
        event.setAccepted(True)
        event.ignore()

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def refresh_combo_box(comboBox, text):
    """Auxiliary function refreshing combo box with a given text.
    """
    idx = comboBox.findText(text)
    comboBox.blockSignals(True)
    if idx != -1:
        comboBox.setCurrentIndex(idx)
        comboBox.blockSignals(False)
        return True
    else:
        comboBox.setCurrentIndex(0)
        comboBox.blockSignals(False)
        return False
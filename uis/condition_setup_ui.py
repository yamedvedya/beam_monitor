# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/p23user/utils/beam_monitor/uis/condition_setup.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConditionSetup(object):
    def setupUi(self, ConditionSetup):
        ConditionSetup.setObjectName("ConditionSetup")
        ConditionSetup.resize(258, 147)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConditionSetup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(ConditionSetup)
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lb_name = QtWidgets.QLabel(ConditionSetup)
        self.lb_name.setMinimumSize(QtCore.QSize(0, 30))
        self.lb_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_name.setObjectName("lb_name")
        self.horizontalLayout_3.addWidget(self.lb_name)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ConditionSetup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(ConditionSetup)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cmb_condition = QtWidgets.QComboBox(ConditionSetup)
        self.cmb_condition.setObjectName("cmb_condition")
        self.cmb_condition.addItem("")
        self.cmb_condition.addItem("")
        self.cmb_condition.addItem("")
        self.horizontalLayout_2.addWidget(self.cmb_condition)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConditionSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConditionSetup)
        self.buttonBox.accepted.connect(ConditionSetup.accept)
        self.buttonBox.rejected.connect(ConditionSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ConditionSetup)

    def retranslateUi(self, ConditionSetup):
        _translate = QtCore.QCoreApplication.translate
        ConditionSetup.setWindowTitle(_translate("ConditionSetup", "Dialog"))
        self.label_4.setText(_translate("ConditionSetup", "Condition"))
        self.lb_name.setText(_translate("ConditionSetup", "TextLabel"))
        self.label.setText(_translate("ConditionSetup", "Threshold:"))
        self.label_2.setText(_translate("ConditionSetup", "Type"))
        self.cmb_condition.setItemText(0, _translate("ConditionSetup", "Equal"))
        self.cmb_condition.setItemText(1, _translate("ConditionSetup", "Less"))
        self.cmb_condition.setItemText(2, _translate("ConditionSetup", "More"))


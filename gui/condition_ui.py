# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/condition.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_condition(object):
    def setupUi(self, condition):
        condition.setObjectName("condition")
        condition.resize(256, 65)
        self.gridLayout = QtWidgets.QGridLayout(condition)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(condition)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 4)
        self.line_4 = QtWidgets.QFrame(condition)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 1, 0, 1, 1)
        self.lb_Caption = QtWidgets.QLabel(condition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lb_Caption.setFont(font)
        self.lb_Caption.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_Caption.setObjectName("lb_Caption")
        self.gridLayout.addWidget(self.lb_Caption, 1, 1, 1, 1)
        self.lb_State = QtWidgets.QLabel(condition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lb_State.setFont(font)
        self.lb_State.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_State.setObjectName("lb_State")
        self.gridLayout.addWidget(self.lb_State, 1, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(condition)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(condition)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 4)

        self.retranslateUi(condition)
        QtCore.QMetaObject.connectSlotsByName(condition)

    def retranslateUi(self, condition):
        _translate = QtCore.QCoreApplication.translate
        condition.setWindowTitle(_translate("condition", "Form"))
        self.lb_Caption.setText(_translate("condition", "nm"))
        self.lb_State.setText(_translate("condition", "eV"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading uis file 'D:/p22code/monitor/uis/condition.uis'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_condition(object):
    def setupUi(self, condition):
        condition.setObjectName(_fromUtf8("condition"))
        condition.resize(237, 99)
        self.gridLayout = QtGui.QGridLayout(condition)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(condition)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 4)
        self.line_4 = QtGui.QFrame(condition)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 1, 0, 1, 1)
        self.lb_Caption = QtGui.QLabel(condition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lb_Caption.setFont(font)
        self.lb_Caption.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_Caption.setObjectName(_fromUtf8("lb_Caption"))
        self.gridLayout.addWidget(self.lb_Caption, 1, 1, 1, 1)
        self.lb_State = QtGui.QLabel(condition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lb_State.setFont(font)
        self.lb_State.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_State.setObjectName(_fromUtf8("lb_State"))
        self.gridLayout.addWidget(self.lb_State, 1, 2, 1, 1)
        self.line_3 = QtGui.QFrame(condition)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 1, 3, 1, 1)
        self.line_2 = QtGui.QFrame(condition)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 4)

        self.retranslateUi(condition)
        QtCore.QMetaObject.connectSlotsByName(condition)

    def retranslateUi(self, condition):
        condition.setWindowTitle(_translate("condition", "Form", None))
        self.lb_Caption.setText(_translate("condition", "nm", None))
        self.lb_State.setText(_translate("condition", "eV", None))


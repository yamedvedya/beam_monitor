# -*- coding: utf-8 -*-

# Form implementation generated from reading uis file 'D:/p22code/monitor/uis/mainwindow.uis'
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

class Ui_Beam_Monitor(object):
    def setupUi(self, Beam_Monitor):
        Beam_Monitor.setObjectName(_fromUtf8("Beam_Monitor"))
        Beam_Monitor.resize(1278, 356)
        self.centralwidget = QtGui.QWidget(Beam_Monitor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(500, 0))
        font = QtGui.QFont()
        font.setPointSize(62)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lbStatus = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        self.lbStatus.setFont(font)
        self.lbStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lbStatus.setObjectName(_fromUtf8("lbStatus"))
        self.horizontalLayout.addWidget(self.lbStatus)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layout_conditions = QtGui.QWidget(self.centralwidget)
        self.layout_conditions.setMinimumSize(QtCore.QSize(330, 0))
        self.layout_conditions.setObjectName(_fromUtf8("layout_conditions"))
        self.verticalLayout.addWidget(self.layout_conditions)
        Beam_Monitor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Beam_Monitor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1278, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Beam_Monitor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Beam_Monitor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Beam_Monitor.setStatusBar(self.statusbar)

        self.retranslateUi(Beam_Monitor)
        QtCore.QMetaObject.connectSlotsByName(Beam_Monitor)

    def retranslateUi(self, Beam_Monitor):
        Beam_Monitor.setWindowTitle(_translate("Beam_Monitor", "MainRoutine", None))
        self.label.setText(_translate("Beam_Monitor", "Beam:", None))
        self.lbStatus.setText(_translate("Beam_Monitor", "OFF!!!", None))


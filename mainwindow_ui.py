# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/p22user/p22ectrl/LM4_monitor/mainwindow.ui'
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

class Ui_LM4_Monitor(object):
    def setupUi(self, LM4_Monitor):
        LM4_Monitor.setObjectName(_fromUtf8("LM4_Monitor"))
        LM4_Monitor.resize(1219, 219)
        self.centralwidget = QtGui.QWidget(LM4_Monitor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(750, 0))
        font = QtGui.QFont()
        font.setPointSize(52)
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
        LM4_Monitor.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(LM4_Monitor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1219, 30))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        LM4_Monitor.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(LM4_Monitor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        LM4_Monitor.setStatusBar(self.statusbar)

        self.retranslateUi(LM4_Monitor)
        QtCore.QMetaObject.connectSlotsByName(LM4_Monitor)

    def retranslateUi(self, LM4_Monitor):
        LM4_Monitor.setWindowTitle(_translate("LM4_Monitor", "MainWindow", None))
        self.label.setText(_translate("LM4_Monitor", "Beam status:", None))
        self.lbStatus.setText(_translate("LM4_Monitor", "OFF!!!", None))


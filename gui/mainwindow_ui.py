# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Beam_Monitor(object):
    def setupUi(self, Beam_Monitor):
        Beam_Monitor.setObjectName("Beam_Monitor")
        Beam_Monitor.resize(1000, 356)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Beam_Monitor.sizePolicy().hasHeightForWidth())
        Beam_Monitor.setSizePolicy(sizePolicy)
        Beam_Monitor.setMinimumSize(QtCore.QSize(1000, 0))
        Beam_Monitor.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.centralwidget = QtWidgets.QWidget(Beam_Monitor)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(320, 0))
        self.label.setMaximumSize(QtCore.QSize(320, 16777215))
        font = QtGui.QFont()
        font.setPointSize(62)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lbStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbStatus.setMinimumSize(QtCore.QSize(450, 0))
        self.lbStatus.setMaximumSize(QtCore.QSize(450, 16777215))
        font = QtGui.QFont()
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        self.lbStatus.setFont(font)
        self.lbStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lbStatus.setObjectName("lbStatus")
        self.horizontalLayout.addWidget(self.lbStatus)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layout_conditions = QtWidgets.QWidget(self.centralwidget)
        self.layout_conditions.setMinimumSize(QtCore.QSize(330, 0))
        self.layout_conditions.setObjectName("layout_conditions")
        self.verticalLayout.addWidget(self.layout_conditions)
        Beam_Monitor.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Beam_Monitor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        Beam_Monitor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Beam_Monitor)
        self.statusbar.setObjectName("statusbar")
        Beam_Monitor.setStatusBar(self.statusbar)

        self.retranslateUi(Beam_Monitor)
        QtCore.QMetaObject.connectSlotsByName(Beam_Monitor)

    def retranslateUi(self, Beam_Monitor):
        _translate = QtCore.QCoreApplication.translate
        Beam_Monitor.setWindowTitle(_translate("Beam_Monitor", "Beam monitor"))
        self.label.setText(_translate("Beam_Monitor", "Beam:"))
        self.lbStatus.setText(_translate("Beam_Monitor", "OFF!!!"))

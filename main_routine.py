import PyTango
import playsound
from notify_run import Notify
import time

from PyQt4 import QtGui, QtCore
from mainwindow_ui import Ui_LM4_Monitor


# ----------------------------------------------------------------------
class MainRoutine(QtGui.QMainWindow):

    SoundRepeatTime = 1

    # ----------------------------------------------------------------------
    def __init__(self, options):
        """
        """
        super(MainRoutine, self).__init__()

        # GUI
        self._ui = Ui_LM4_Monitor()
        self._ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setupMenu()

        self.notifyChannel = Notify('https://notify.run/api/', 'https://notify.run/WBYSjwtglRmFnrxC')
        self.backNotificationSent = False
        self.lostNotificationSent = False

        self.playSound = True
        self.lastSoundTime = time.time()
        self.status = False

        self.statusBarLabel = QtGui.QLabel("Sound: {}".format(str(self.playSound)))
        self.statusBar().addPermanentWidget(self.statusBarLabel)

        self._serverPort = options.port
        self.LM4_proxy   = PyTango.DeviceProxy('hasylab/p22_lm4/output')
        self.V2_proxy    = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/v2')
        self.PS2_proxy   = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/ps2')
        self.PETRA_proxy = PyTango.DeviceProxy('petra/globals/keywords')
        self.DCM_proxy   = PyTango.DeviceProxy('p22/dcmener/oh.01')

        self.sound = options.sound

        self._refreshTimer = QtCore.QTimer(self)
        self._refreshTimer.timeout.connect(self._refreshStatus)
        self._refreshTimer.start(500)

        self.exitOnClose = False

    # ----------------------------------------------------------------------
    def setupMenu(self):

        self._soundAction = QtGui.QAction("Turn off sound", self,
                                               triggered=self._trunOnSound)
        self._soundAction.setCheckable(True)

        self._closeAction = QtGui.QAction("Exit", self,
                                          triggered=self._quitMe)

        self._menuComponents = QtGui.QMenu("Values to be monitored", self)

        self._monitorLM4 = QtGui.QAction("Monitor LM4", self)
        self._monitorLM4.setCheckable(True)
        self._monitorLM4.setChecked(True)

        self._monitorV2 = QtGui.QAction("Monitor V2", self)
        self._monitorV2.setCheckable(True)
        self._monitorV2.setChecked(True)

        self._monitorPS2 = QtGui.QAction("Monitor PS2", self)
        self._monitorPS2.setCheckable(True)
        self._monitorPS2.setChecked(True)

        self._monitorPETRAcurrent = QtGui.QAction("Monitor PETRA current", self)
        self._monitorPETRAcurrent.setCheckable(True)
        self._monitorPETRAcurrent.setChecked(True)

        self._monitorPETRAbunches = QtGui.QAction("Monitor PETRA bunches", self)
        self._monitorPETRAbunches.setCheckable(True)
        self._monitorPETRAbunches.setChecked(True)

        self._menuComponents.addAction(self._monitorLM4)
        self._menuComponents.addAction(self._monitorV2)
        self._menuComponents.addAction(self._monitorPS2)
        self._menuComponents.addAction(self._monitorPETRAcurrent)
        self._menuComponents.addAction(self._monitorPETRAbunches)

        menubar = self.menuBar()
        menubar.addAction(self._soundAction)
        self._soundAction.setEnabled(False)
        menubar.addAction(self._menuComponents.menuAction())
        menubar.addAction(self._closeAction)

    # ----------------------------------------------------------------------
    def _sendTest(self):

        self.notifyChannel.send('Test!')

    # ----------------------------------------------------------------------
    def _refreshStatus(self):

        try:
            maxLm4 = self.LM4_proxy.Frame.max()
        except:
            maxLm4 = False

        try:
            v2State = self.V2_proxy.stellung[0]
        except:
            v2State = False

        try:
            PBunches = self.PETRA_proxy.NumberOfBunches
            gotPbunches = True
        except:
            gotPbunches = False

        try:
            PCurrent = self.PETRA_proxy.BeamCurrent
            gotPcurrent = True
        except:
            gotPcurrent = False

        try:
            ps2State = self.PS2_proxy.stellung[0]
        except:
            ps2State = False

        try:
            energyText = "{:.2f} eV".format(self.DCM_proxy.position)
        except:
            energyText = 'OK'

        beamOk = True

        if v2State:
            if int(v2State) != 2:
                if self._monitorV2.isChecked():
                    beamOk = False
                self._ui.lbV2.setText("closed")
                self._ui.lbV2.setStyleSheet('color: red')
            else:
                self._ui.lbV2.setText("open")
                self._ui.lbV2.setStyleSheet('color: green')
        else:
            self._ui.lbV2.setText("NC")
            self._ui.lbV2.setStyleSheet('color: orange')

        if maxLm4:
            if maxLm4 < 50:
                if self._monitorLM4.isChecked():
                    beamOk = False
                self._ui.lbLM4.setText("no beam")
                self._ui.lbLM4.setStyleSheet('color: red')
            else:
                self._ui.lbLM4.setText("OK")
                self._ui.lbLM4.setStyleSheet('color: green')
        else:
            self._ui.lbLM4.setText("NC")
            self._ui.lbLM4.setStyleSheet('color: orange')

        if gotPbunches:
            self._ui.lbPbunches.setText('{}'.format(int(PBunches)))
            if int(PBunches) in [40, 80, 480]:
                self._ui.lbPbunches.setStyleSheet('color: green')
            else:
                if self._monitorPETRAbunches.isChecked():
                    beamOk = False
                self._ui.lbPbunches.setStyleSheet('color: red')
        else:
            self._ui.lbPbunches.setText('NC')
            self._ui.lbPbunches.setStyleSheet('color: orange')


        if gotPcurrent:
            self._ui.lbPcurrent.setText('{}'.format(int(PCurrent)))
            if int(PCurrent) < 60:
                if self._monitorPETRAcurrent.isChecked():
                    beamOk = False
                self._ui.lbPcurrent.setStyleSheet('color: red')
            elif int(PCurrent) < 65:
                self._ui.lbPcurrent.setStyleSheet('color: orange')
            else:
                self._ui.lbPcurrent.setStyleSheet('color: green')
        else:
            self._ui.lbPcurrent.setText('NC')
            self._ui.lbPcurrent.setStyleSheet('color: orange')

        if ps2State:
            if int(ps2State) != 2:
                if self._monitorPS2.isChecked():
                    beamOk = False
                self._ui.lbPS2.setText("closed")
                self._ui.lbPS2.setStyleSheet('color: red')
            else:
                self._ui.lbPS2.setText("open")
                self._ui.lbPS2.setStyleSheet('color: green')
        else:
            self._ui.lbPS2.setText("NC")
            self._ui.lbPS2.setStyleSheet('color: orange')

        if not beamOk:
            self.status = False
            self._ui.lbStatus.setText("not OK")
            self._ui.lbStatus.setStyleSheet('color: red')

            if self.playSound:
                if time.time() > self.lastSoundTime + self.SoundRepeatTime:
                    self.lastSoundTime = time.time()
                    self._soundAction.setText('Turn off sound')
                    self._soundAction.setEnabled(True)
                    playsound.playsound('./{}.mp3'.format(self.sound), True)

            if not self.lostNotificationSent:
                self.notifyChannel.send('Beam lost')
                self.backNotificationSent = False
                self.lostNotificationSent = True
        else:
            self.playSound = True
            self._soundAction.setEnabled(False)
            self.status = True
            self._ui.lbStatus.setText(energyText)
            self._ui.lbStatus.setStyleSheet('color: green')

            if not self.backNotificationSent:
                self.notifyChannel.send('Beam back')
                self.backNotificationSent = True
                self.lostNotificationSent = False

        self.statusBarLabel.setText("Sound: {}".format(str(self.playSound)))

    # ----------------------------------------------------------------------
    def _trunOnSound(self):
        self.playSound = not self.playSound
        if self.playSound:
            self._soundAction.setText('Turn off sound')
        else:
            self._soundAction.setText('Turn on sound')

    # ----------------------------------------------------------------------
    def _startServer(self):
        if not self._thread_running:
            self.run()
        else:
            self.stopServerBucket.put('1')

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        if self.exitOnClose:
            # self.stopServerBucket.put('1')
            event.accept()
        else:
            event.setAccepted(True)
            event.ignore()

    # ----------------------------------------------------------------------
    def _showMe(self):
        self.show()
    #----------------------------------------------------------------------
    def _quitMe(self):
        self.exitOnClose = True
        self.close()
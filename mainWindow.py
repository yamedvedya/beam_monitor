import PyTango
import playsound
from notify_run import Notify

import socket
import select
import traceback
import json

from PyQt4 import QtGui, QtCore
from mainwindow_ui import Ui_LM4_Monitor

# from Queue import Queue
# from Queue import Empty as emptyQueue

# ----------------------------------------------------------------------
class MainWindow(QtGui.QMainWindow):

    # ----------------------------------------------------------------------
    def __init__(self, options):
        """
        """
        super(MainWindow, self).__init__()

        # GUI
        self._ui = Ui_LM4_Monitor()
        self._ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setupMenu()

        self.notifyChannel = Notify('https://notify.run/api/', 'https://notify.run/WBYSjwtglRmFnrxC')
        self.backNotificationSent = False
        self.lostNotificationSent = False

        self.playSound = True
        self.status = False

        self.statusBarLabel = QtGui.QLabel("Sound: {}".format(str(self.playSound)))
        self.statusBar().addPermanentWidget(self.statusBarLabel)

        self._serverPort = options.port
        self.LM4_proxy = PyTango.DeviceProxy('hasylab/p22_lm4/output')
        self.V2_proxy = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/v2')
        self.PS2_proxy = PyTango.DeviceProxy('hasylab/petra3_p22vil.cdi/ps2')
        self.PETRA_proxy = PyTango.DeviceProxy('petra/globals/keywords')

        self.sound = options.sound

        # self.stopServerBucket = Queue()
        # self._thread_running = False
        # self._startServer()

        self._refreshTimer = QtCore.QTimer(self)
        self._refreshTimer.timeout.connect(self._refreshStatus)
        self._refreshTimer.start(500)

        self.exitOnClose = False

        self.CMD_MAP = {"Disconnect": self._disconnect,
                        "Status": self._getStatus,
                       }
    # ----------------------------------------------------------------------
    def setupMenu(self):

        self._soundAction = QtGui.QAction("Turn off sound", self,
                                               triggered=self._trunOnSound)

        self._serverAction = QtGui.QAction("Stop server", self,
                                               triggered=self._startServer)

        self._closeAction = QtGui.QAction("Exit", self,
                                               triggered=self._quitMe)

        self._testMessage = QtGui.QAction("Test Notify", self,
                                               triggered=self._sendTest)

        menubar = self.menuBar()
        menubar.addAction(self._soundAction)
        self._soundAction.setEnabled(False)
        # menubar.addAction(self._serverAction)
        # menubar.addAction(self._testMessage)
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
            PCurrent = self.PETRA_proxy.BeamCurrent
            gotPETRA = True
        except:
            gotPETRA = False

        try:
            ps2State = self.PS2_proxy.stellung[0]
        except:
            ps2State = False

        beamOk = True

        if v2State:
            if int(v2State) != 2:
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
            if maxLm4 < 15:
                beamOk = False
                self._ui.lbLM4.setText("no beam")
                self._ui.lbLM4.setStyleSheet('color: red')
            else:
                self._ui.lbLM4.setText("OK")
                self._ui.lbLM4.setStyleSheet('color: green')
        else:
            self._ui.lbLM4.setText("NC")
            self._ui.lbLM4.setStyleSheet('color: orange')

        if gotPETRA:
            self._ui.lbPetra.setText('{}'.format(int(PCurrent)))
            if int(PCurrent) < 80:
                beamOk = False
                self._ui.lbPetra.setStyleSheet('color: red')
            elif int(PCurrent) < 98:
                self._ui.lbPetra.setStyleSheet('color: orange')
            else:
                self._ui.lbPetra.setStyleSheet('color: green')
        else:
            self._ui.lbPetra.setText('NC')
            self._ui.lbPetra.setStyleSheet('color: orange')

        if ps2State:
            if int(ps2State) != 2:
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
            self._ui.lbStatus.setText("OK")
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

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def run(self):
        """
        """
        print ("VISA Gate server on port {}".format(self._serverPort))

        self._socket.listen(1)
        self._thread_running = True

        read_list = [self._socket]
        while True:
            readable, writable, errored = select.select(read_list, [], [], 0.1)
            for s in readable:
                if s is self._socket:
                    self._connection, client_address = self._socket.accept()
                    self._connection.setblocking(0)
                    print('Test')
                    while True:
                        try:
                            self._process_request()
                        except socket.error as err:
                            if err.args[0] == 10035:
                                try:
                                    _ = self.stopBucket.get(block=False)
                                except emptyQueue:
                                    pass
                                else:
                                    self.stopBucket.put('1')
                                    break
                            else:
                                break
                        except Exception as _:
                            self.newPrint(traceback.format_exc())
                            self.stopBucket.put('1')
                            break
            try:
                _ = self.stopBucket.get(block=False)
            except emptyQueue:
                pass
            else:
                break

    # ----------------------------------------------------------------------
    def _process_request(self):
        """
        """
        try:
            request = str(
                self._connection.recv(self.MAX_REQUEST_LEN)).strip()  # NOTE: won't work in Python 3
            status, reply = self._command_dispatcher(request)

            self.newPrint("Request: '{}', status: '{}', reply: '{}'".format(request, status, reply))
            self._connection.sendall(json.dumps([status, reply]))

        except KillConnection as _:
            self.newPrint(traceback.format_exc())
            self._connection.close()
            self.newPrint("Connection closed")
            raise

    # ----------------------------------------------------------------------
    def _command_dispatcher(self, request):

        split = request.split('#')
        command = split[0]
        params = ""

        if len(split) > 1:
            params = split[1:]
        try:
            return self.CMD_MAP[command](params)
        except KeyError as err:
            return False, 'KeyError'

    # ----------------------------------------------------------------------
    def _getStatus(self):

        self._refreshStatus()
        return self.status

    # ----------------------------------------------------------------------
    def _disconnect(self, params):

        raise KillConnection()             # should close connection

# ----------------------------------------------------------------------
class KillConnection(Exception):
    pass
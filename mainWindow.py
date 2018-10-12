import PyTango
import playsound

import socket
import select
import traceback
import json

from PyQt4 import QtGui, QtCore
from mainwindow_ui import Ui_LM4_Monitor

from Queue import Queue
from Queue import Empty as emptyQueue

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

        self.playSound = False
        self.status = False

        self._serverPort = options.port
        self.device_proxy = PyTango.DeviceProxy(options.device)

        self.sound = options.sound

        self.stopServerBucket = Queue()
        self._thread_running = False

        self._refreshTimer = QtCore.QTimer(self)
        self._refreshTimer.timeout.connect(self._refreshStatus)
        self._refreshTimer.start(1000)

        self.exitOnClose = False

        self.CMD_MAP = {"Disconnect": self._disconnect,
                        "Status": self._getStatus,
                       }
    # ----------------------------------------------------------------------
    def setupMenu(self):

        self._soundAction = QtGui.QAction("Turn on sound", self,
                                               triggered=self._trunOnSound)

        self._serverAction = QtGui.QAction("Start server", self,
                                               triggered=self._startServer)

        self._closeAction = QtGui.QAction("Exit", self,
                                               triggered=self._quitMe)

        menubar = self.menuBar()
        menubar.addAction(self._soundAction)
        menubar.addAction(self._serverAction)
        menubar.addAction(self._closeAction)

    # ----------------------------------------------------------------------
    def _refreshStatus(self):
        frame = self.device_proxy.Frame
        if self.device_proxy.Frame.max() < 15:
            self.status = False
            self._ui.lbStatus.setText("OFF!!!")
            self._ui.lbStatus.setStyleSheet('color: red')

            if self.playSound:
                playsound.playsound('./{}.mp3'.format(self.sound), True)

        else:
            self.status = True
            self._ui.lbStatus.setText("ON")
            self._ui.lbStatus.setStyleSheet('color: green')

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
            self._worker.start()
        else:
            self.stopServerBucket.put('1')

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        if self.exitOnClose:
            self.stopServerBucket.put('1')
            event.accept()
        else:
            event.setAccepted(True)
            event.ignore()

    # ----------------------------------------------------------------------
    def _showMe(self):
        self.show()
    # ----------------------------------------------------------------------
    def _quitMe(self):
        self.exitOnClose = True
        self.close()

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def run(self):
        """
        """
        print ("VISA Gate server on port {}".format(self.port))

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
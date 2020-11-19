from src.propagating_thread import ExcThread
from queue import Queue
from settings import *

import socket
import select
import traceback
import json
import time


class Info_Server(object):

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def __init__(self, host='', port=None, parent=None):

        self.host = host
        self.port = port

        self.parent = parent

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self._socket.listen(1)
        self._socket.bind((self.host, self.port))

        self._connectionMap = []
        self._server_mode = 'idle'
        self.errorQueue = Queue()
        self._serverWorker = ExcThread(self.runServer, 'server', self.errorQueue)

        self.CMD_MAP = {"status": self._status,
                        "closeConnection": self._closeConnection
                        }

        self._serverWorker.start()

    # ----------------------------------------------------------------------
    def stop_server(self):
        self._serverWorker.stop()
        while self._server_mode != 'idle':
            time.sleep(0.1)

    # ----------------------------------------------------------------------
    def runServer(self):
        """
        """
        print("Beamline Status server on port {}".format(self.port))

        self._socket.listen(MAX_CLIENT_NUMBER)
        self._server_mode = 'running'

        read_list = [self._socket]
        while not self._serverWorker.stopped():
            readable, writable, errored = select.select(read_list, [], [], 0.1)
            for s in readable:
                if s is self._socket:
                    connection, address = self._socket.accept()
                    connection.setblocking(False)
                    self._connectionMap.append([connection, address])
                    print('New client added: {:s}'.format(address))

            for connection, address in self._connectionMap:
                try:
                    request = connection.recv(MAX_REQUEST_LEN).decode()
                    if request:
                        connection.sendall(self._process_request(request).encode())
                    else:
                        print('Client closed: {:s}'.format(address))
                        connection.close()
                        self._connectionMap.remove([connection, address])

                except socket.error as err:
                    if err.args[0] == 10035:
                        if self._serverWorker.stopped():
                            break
                    elif err.errno == 11:
                        time.sleep(0.1)
                    elif err.errno == 10054:
                        print('Client closed: {:s}'.format(address))
                        connection.close()
                        self._connectionMap.remove([connection, address])
                    else:
                        pass

                except KillConnection as _:
                    print(traceback.format_exc())
                    print('Client closed: {:s}'.format(address))
                    connection.close()
                    self._connectionMap.remove([connection, address])

                except Exception as _:
                    print(traceback.format_exc())
                    break

        self._socket.close()
        print('Server closed')
        self._server_mode = 'idle'

    # ----------------------------------------------------------------------
    def _process_request(self, request):
        """
        """
        request = str(request).strip()
        status, reply = self._command_dispatcher(request)
        print("Request: {}, Reply: status: '{}', reply: '{}'".format(request, status, reply))
        return json.dumps([status, reply])

    # ----------------------------------------------------------------------
    def _dummyMode(self, mode):

        self._dummyMode = True

    # ----------------------------------------------------------------------
    def _command_dispatcher(self, request):

        split = request.split(' ')
        try:
            return self.CMD_MAP[split[0]]
        except KeyError as err:
            return False, 'KeyError'

    # ----------------------------------------------------------------------
    def _status(self):

        return True, self.parent.beam_status

    # ----------------------------------------------------------------------
    def _closeConnection(self, params):

        raise KillConnection()  # should close connection

# ----------------------------------------------------------------------
class KillConnection(Exception):
    pass
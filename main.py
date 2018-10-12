import sys

from PyQt4 import QtGui
from mainWindow import MainWindow
from optparse import OptionParser

# ----------------------------------------------------------------------
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port",
                      help="Port number", default="16985")
    parser.add_option("-d", "--device", dest="device",
                      help="Device server", default='''hasylab/p22_lm4/Output''')
    parser.add_option("-s", "--sound", dest="sound",
                      help="Sound file", default='''Fire''')
    (options, _) = parser.parse_args()

    app = QtGui.QApplication(sys.argv)          # don't pass any args here!

    mainWindow = MainWindow(options)
    mainWindow.show()

    code = app.exec_()
    sys.exit(code)

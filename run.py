# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------

import sys

from PyQt5 import QtWidgets
from src.main_routine import MainRoutine
from optparse import OptionParser


def move2RightBottomCorner(win):
    screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
    screen_size = (screen_geometry.width(), screen_geometry.height())
    win_size = (win.frameSize().width(), win.frameSize().height())
    x = screen_size[0] - win_size[0]
    y = screen_size[1] - win_size[1]
    win.move(x, y)

# ----------------------------------------------------------------------
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-w", "--windowless", dest="windowless",
                      help="True or False", default='False')
    parser.add_option("-s", "--sound", dest="sound",
                      help="Sound file", default='Fire')
    parser.add_option("-a", "--alarm", dest="alarm",
                      help="True or False", default='True')
    parser.add_option("-m", "--msgbox", dest="msgbox",
                      help="True or False", default='False')
    parser.add_option("-n", "--notify", dest="notify",
                      help="True or False", default='False')
    parser.add_option("-p", "--port", dest="port",
                      help="Server port", default='30786')
    (options, _) = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)          # don't pass any args here!

    mainWindow = MainRoutine(options)
    mainWindow.move(mainWindow.width() * -3, 0)
    mainWindow.show()

    move2RightBottomCorner(mainWindow)

    code = app.exec_()
    sys.exit(code)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Author:        sebastian.piec@desy.de
# Last modified: 2017, July 5
# ----------------------------------------------------------------------

"""Compiles ui and rcc files (works on Linux/Windows, with PyQt/PySide).

Usage:
     ./build.py [qtlib] [os]

e.g.:
     ./build.py pyqt linux
     ./build.py pyside windows
"""

from __future__ import print_function

import os
import sys

# ----------------------------------------------------------------------

ui_compilers = {"linux": {
    "pyqt": "pyuic4",
    "pyside": "pyside-uic"
},
    "windows": {
        "pyqt": "E:\\Python27\\lib\\site-packages\\PyQt4\\pyuic4.bat",
        "pyside": ""
    }
}

rc_compilers = {"linux": {
    "pyqt": "pyrcc4",
    "pyside": "pyside-rcc"
},
    "windows": {
        "pyqt": "E:\\Python27\\lib\\site-packages\\PyQt4\\pyrcc4.bat",
        "pyside": ""
    }
}


# ----------------------------------------------------------------------
def compile_uis(ui_compiler, rc_compiler, pathname):
    """
    """
    for f in [f for f in os.listdir(pathname) if os.path.isfile(os.path.join(pathname, f))
                                               and os.path.splitext(f)[-1] in [".ui",
                                                                               ".qrc"]]:  # simplify this loop TODO
        base, ext = os.path.splitext(f)
        post, comp = ("_ui", ui_compiler) if ext == ".ui" else ("_rc", rc_compiler)

        cmd = "{} {}/{} -o {}/{}{}.py".format(comp, pathname, f, pathname, base, post)
        print(cmd)
        os.system(cmd)


# ----------------------------------------------------------------------
if __name__ == "__main__":

    pathname = os.path.dirname(sys.argv[0])

    lib_name, sys_name = "pyqt", "linux"

    if len(sys.argv) > 1:
        lib_name = sys.argv[1].lower()

    if len(sys.argv) > 2:
        sys_name = sys.argv[2].lower()

    compile_uis(ui_compilers[sys_name][lib_name],
                rc_compilers[sys_name][lib_name], pathname)

    print("All OK!")


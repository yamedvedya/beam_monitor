# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------


from __future__ import print_function

import os
import sys

# ----------------------------------------------------------------------

ui_compilers = {"linux": {
    "pyqt": "python -m PyQt5.uic.pyuic",
},
    "windows": {
        "pyqt": "C://Users//matveyev//AppData//Local//Programs//Python//Python37-32//Scripts//pyuic5.exe",
    }
}

# ----------------------------------------------------------------------
def compile_uis(ui_compiler, sourcepath):
    """
    """
    for f in [f for f in os.listdir(sourcepath) if os.path.isfile(os.path.join(sourcepath, f))
                                               and os.path.splitext(f)[-1] in [".ui"]]:
        base, ext = os.path.splitext(f)
        post, comp = ("_ui", ui_compiler)

        cmd = "{} {}/{} -o {}/{}{}.py".format(comp, sourcepath, f, sourcepath, base, post)
        print(cmd)
        os.system(cmd)


# ----------------------------------------------------------------------
if __name__ == "__main__":

    sourcepath = os.path.dirname(sys.argv[0]) + '/uis'

    lib_name, sys_name = "pyqt", "linux"
    if len(sys.argv) > 1:
        lib_name = sys.argv[1].lower()

    if len(sys.argv) > 2:
        sys_name = sys.argv[2].lower()

    compile_uis(ui_compilers[sys_name][lib_name], sourcepath)

    print("All OK!")


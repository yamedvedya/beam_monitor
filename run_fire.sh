# ----------------------------------------------------------------------
# Author:   y.matveev@gmail.com
# Modified: 26/02/2020
# ----------------------------------------------------------------------

BASEDIR=`dirname $0`
cd $BASEDIR

export VIEWERPATH=$PWD/
export PYTHONPATH=$PYTHONPATH:$VIEWERPATH
./venv/bin/python ./run.py --sound="Fire"
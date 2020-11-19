BASEDIR=`dirname $0`
cd $BASEDIR

export VIEWERPATH=$PWD/
export PYTHONPATH=$PYTHONPATH:$VIEWERPATH

python3 -m venv venv
source venv/bin/activate
pip install notify-run
pip install playsound
pip install PyQt5
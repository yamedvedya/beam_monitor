'''
Created by matveyev at 05.12.2022

inspired by playsound
'''

from os.path import abspath

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from urllib.request import pathname2url
from threading import Thread
import logging

from beamline_monitor import APP_NAME

logger = logging.getLogger(APP_NAME)


class PlayAlarm(Thread):

    # ----------------------------------------------------------------------
    def __init__(self, sound):
        super(PlayAlarm, self).__init__()
    # pathname2url escapes non-URL-safe characters

        Gst.init(None)

        self.playbin = Gst.ElementFactory.make('playbin', 'playbin')
        self.playbin.props.uri = 'file://' + pathname2url(abspath(sound))

        set_result = self.playbin.set_state(Gst.State.PLAYING)
        if set_result != Gst.StateChangeReturn.ASYNC:
            msg = "playbin.set_state returned " + repr(set_result)
            # logger.error(msg)
            raise RuntimeError(msg)

    # ----------------------------------------------------------------------
    def run(self) -> None:
        logger.debug('Starting alarm')
        bus = self.playbin.get_bus()
        try:
            bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
        finally:
            self.playbin.set_state(Gst.State.NULL)

        logger.debug('Finishing alarm')
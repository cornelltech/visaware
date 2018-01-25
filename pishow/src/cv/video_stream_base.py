"""video_stream_base.py"""

import abc
import sys
import cv2
import numpy
import unittest
from threading import Thread
from pacer import Pacer


DEFAULT_FPS = 30.0

class VideoStreamBase:
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, fps=DEFAULT_FPS):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.fps = fps
        self.pacer = Pacer(fps)
        self.stopped = True
        self.stream = None
        self.frame = None

    def start(self):
        # start a thread to read frames from the file video stream
        if self.stream is None:
            raise Exception("Cannot start thread - stream is None")
        if not self.stopped:
            raise Exception("Cannot start thread - a thread is already running")
        self.stopped = False
        thread = Thread(target=self.main_thread, args=())
        thread.daemon = True
        thread.start()
        self.pacer.start()

        return self

    @abc.abstractmethod
    def loop_body(self):
        raise Exception("Not implemented")

    def main_thread(self):
        # keep looping infinitely
        while True:
            if self.stopped:
                return

            self.loop_body()

            if self.fps != 0:
                self.pacer.update()

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

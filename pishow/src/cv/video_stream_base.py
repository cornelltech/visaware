#!/usr/bin/env python
"""file_video_stream.py"""

import abc
import sys
import cv2
import numpy
import unittest
from threading import Thread
from fps import FPS
from pacer import Pacer
# import looper


DEFAULT_FPS = 30

class VideoStreamBase:
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, path, fps=DEFAULT_FPS):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.fps = fps
        self.pacer = Pacer(fps)
        self.stopped = False
        self.stream = None
        self.frame = None

    def start(self):
        # start a thread to read frames from the file video stream

        if self.stream is None:
            raise Exception("Cannot start thread - stream is None")

        thread = Thread(target=self.main_thread, args=())
        thread.daemon = True
        thread.start()
        self.pacer.start()
        return self

    # this is the abstract method that all derived classes must implement
    @abc.abstractmethod
    def main_thread(self):
        # keep looping infinitely
        while True:
            # read the next frame from the file
            (grabbed, frame) = self.stream.read()

            if grabbed:
                self.frame = frame
            else:
                # reached the end of the video file
                self.stop()
                return

            if self.fps:
                self.pacer.update()

    def read(self):
        if self.stopped:
            return None
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        # looper.generic_looper(FileVideoStream(TEST_FILE).start())


if __name__ == "__main__":
    TEST_FILE = "../../../data/vid02.mov"
    unittest.main()

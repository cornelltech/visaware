#!/usr/bin/env python
"""file_video_stream.py"""

import sys
import cv2
import numpy
import unittest
from pacer import Pacer
from video_stream_base import VideoStreamBase
from video_stream_base import DEFAULT_FPS
import looper


class FileVideoStream(VideoStreamBase):
    def __init__(self, path, fps=DEFAULT_FPS):
        super(FileVideoStream, self).__init__(fps)
        self.stream = cv2.VideoCapture(path)

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

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        looper.generic_looper(FileVideoStream(TEST_FILE).start())
        

if __name__ == "__main__":
    TEST_FILE = "../../../data/vid02.mov"
    unittest.main()

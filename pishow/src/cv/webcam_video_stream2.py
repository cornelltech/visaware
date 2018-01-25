#!/usr/bin/env python
"""webcam_video_stream.py"""

import unittest
import cv2
import video_stream_base as base
import looper


class WebcamVideoStream(base.VideoStreamBase):
    def __init__(self, src=0, fps=base.DEFAULT_FPS):
        super(WebcamVideoStream, self).__init__(fps)
        self.stream = cv2.VideoCapture(src)

    def loop_body(self):
        # read the next frame from the file
        (grabbed, frame) = self.stream.read()

        if grabbed:
            self.frame = frame
        else:
            # reached the end of the video file
            self.stop()

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        looper.generic_looper(WebcamVideoStream().start())
              

if __name__ == "__main__":
    unittest.main()

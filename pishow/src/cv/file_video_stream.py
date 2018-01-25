#!/usr/bin/env python
"""file_video_stream.py"""

import sys
import cv2
import numpy
import unittest
from threading import Thread
from fps import FPS
from pacer import Pacer


DEFAULT_FPS = 30

class FileVideoStream:
    def __init__(self, path, fps=DEFAULT_FPS):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        print path
        self.stream = cv2.VideoCapture(path)
        self.pacer = Pacer(fps)
        self.stopped = False
        self.frame = None

    def start(self):
        # start a thread to read frames from the file video stream
        thread = Thread(target=self.main_thread, args=())
        thread.daemon = True
        thread.start()
        self.pacer.start()
        return self

    def main_thread(self):
        # keep looping infinitely
        i = 0
        while True:
            # read the next frame from the file
            (grabbed, frame) = self.stream.read()

            if grabbed:
                self.frame = frame
            else:
                # reached the end of the video file
                self.stop()
                return

            self.pacer.update()
            i += 1

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
        videoStream = FileVideoStream(TEST_FILE).start()
        fps = FPS().start()

        lastFrame = None
        while True:
            frame = videoStream.read()
            if not numpy.array_equal(frame, lastFrame) and frame is not None:
                cv2.imshow('Frame', frame)
                fps.update()

            if videoStream.stopped or cv2.waitKey(1) & 0xFF == ord('q'):
                break

            lastFrame = frame

        fps.stop()
        videoStream.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    TEST_FILE = "../../../data/vid01.mov"
    unittest.main()

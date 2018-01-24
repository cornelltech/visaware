#!/usr/bin/env python
"""fps.py"""

# import the necessary packages

# based on imutils.video package - a drop in replacement for import:
# from imutils.video import FPS

import datetime
import unittest
import time


class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self.startTime = None
        self.endTime = None
        self.nFrames = 0

    def start(self):
        # start the timer
        self.startTime = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self.endTime = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self.nFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self.endTime - self.startTime).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self.nFrames / self.elapsed()

class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        can we instantiate?
        """

        print "[INFO] FPS period: {:.4f}".format(TEST_SLEEP)

        fps = FPS().start()

        while fps.nFrames < N_TEST_FRAMES:
            time.sleep(TEST_SLEEP)
            fps.update()


        fps.stop()
        print "[INFO] elasped time: {:.2f}".format(fps.elapsed())
        print "[INFO] approx. FPS: {:.2f}".format(fps.fps())


if __name__ == "__main__":
    N_TEST_FRAMES = 120
    TEST_FPS = 40.0
    TEST_SLEEP = 1.0/TEST_FPS

    unittest.main()

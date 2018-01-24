#!/usr/bin/env python
"""pacer.py - paced operations"""

import time
import datetime
import unittest
from fps import FPS


class Pacer:
    def __init__(self, desiredFPS):
        """constructor"""
        self.lastIterationTime = None
        self.desiredFPS = desiredFPS
        self.desiredPeriod = 1.0/desiredFPS
        self.timeErrorCorrection = 0

    def start(self):
        """call once, before the loop starts"""
        self.startTime = time.time()
        self.lastIterationTime = self.startTime
        return self

    def update(self):
        """called on each loop iteration, blocks till time is due"""
        now = time.time()
        elapsed = now-self.lastIterationTime
        blockSeconds = self.desiredPeriod-elapsed+self.timeErrorCorrection

        if blockSeconds > 0:
            print "Sleeping {:.2}".format(blockSeconds)
            time.sleep(blockSeconds)
        else:
            # we slept too much perhaps, next time sleep less

            print "NOT Sleeping {:.2}".format(blockSeconds)

        self.timeErrorCorrection = blockSeconds
        self.lastIterationTime = now

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we instantiate? """
        fps = FPS().start()
        pacer = Pacer(DESIRED_FPS).start()

        while fps.nFrames < N_TEST_FRAMES:
            fps.update()
            pacer.update()

        fps.stop()
        print "[INFO] elasped time: {:.2f}".format(fps.elapsed())
        print "[INFO] approx. FPS: {:.2f}".format(fps.fps())


if __name__ == "__main__":
    N_TEST_FRAMES = 120
    DESIRED_FPS = 40.0

    unittest.main()

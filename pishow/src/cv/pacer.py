#!/usr/bin/env python
"""pacer.py - paced operations"""

import time
import unittest
from fps import FPS
import datetime


class Pacer:
    def __init__(self, desiredFPS):
        """constructor"""
        self.startTime = None
        self.lastUpdateTime = None
        self.desiredPeriod = 1.0/desiredFPS
        self.updateError = 0

    def start(self):
        """call once, before the loop starts"""
        self.startTime = time.time()
        self.lastUpdateTime = self.startTime
        return self

    def update(self):
        """called on each loop iteration, blocks till time is due"""
        now = time.time()
        elapsed = now-self.lastUpdateTime
        deltaTime = self.desiredPeriod-elapsed+self.updateError

        if deltaTime > 0:
            # too fast, sleep to wait out full period
            self.updateError = deltaTime
            time.sleep(deltaTime)
        else:
            # too slow, fix the updateError so that next time we sleep less
            self.updateError = 0
            
        self.lastUpdateTime = now

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we instantiate? """
        fps = FPS().start()
        pacer = Pacer(DESIRED_FPS).start()

        while fps.nFrames < N_TEST_FRAMES:
            print datetime.datetime.now()
            fps.update()
            pacer.update()

        fps.stop()
        print "[INFO] elasped time: {:.2f}".format(fps.elapsed())
        print "[INFO] approx. FPS: {:.2f}".format(fps.fps())
        print "[INFO] nFrames: %i" % fps.nFrames


if __name__ == "__main__":
    N_TEST_FRAMES = 200
    DESIRED_FPS = 40.0

    unittest.main()

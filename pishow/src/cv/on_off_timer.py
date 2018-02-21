#!/usr/bin/env python
"""on_off_timer.py - alternates being on and off for specific durations"""

import time


class OnOffTimer(object):
    """Alternate between ON and OFF states for specific durations"""

    def __init__(self, secondsOn, secondsOff, startOn=False):
        """constructor"""
        self.secondsOn = secondsOn
        self.secondsOff = secondsOff
        self.bIsOn = startOn
        timeNow = time.time()
        if startOn:
            self.timeOn = timeNow
            self.timeOff = None
        else:
            self.timeOn = None
            self.timeOff = timeNow

    def is_on(self):
        """
        Returns whether we are on or not right now (first return value of pair),
        but it also returns whether we have just switched state from ON to OFF
        or vice versa.
        """
        timeNow = time.time()
        justSwitched = False
        if self.bIsOn:
            # we are on now
            if timeNow - self.timeOn > self.secondsOn:
                # exceeded the ON time, turn off
                self.bIsOn = False
                self.timeOff = timeNow
                justSwitched = True
        else:
            # we are off now
            if timeNow - self.timeOff > self.secondsOff:
                # exceeded the OFF time, turn on
                self.bIsOn = True
                self.timeOn = timeNow
                justSwitched = True

        return (self.bIsOn, justSwitched)

#!/usr/bin/env python
"""on_off_timer.py - alternates being on and off for specific durations"""


import time


class OnOffTimer(object):
    """like pins-based wall-mounted timers, with randomness"""

    def __init__(self, secondsOn, secondsOff, startTurnedOn=False):
        """constructor"""
        self.secondsOn = secondsOn
        self.secondsOff = secondsOff
        self.bIsOn = startOn
        timeNow = time.time()
        if startOn:
            self.timeTurnedOn = timeNow
            self.timeTurnedOff = None
        else:
            self.timeTurnedOn = None
            self.timeTurnedOff = timeNow

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
            if timeNow - self.timeTurnedOn > self.secondsOn:
                # exceeded the ON time, turn off
                self.bIsOn = False
                self.timeTurnedOff = timeNow
                justSwitched = True
        else:
            # we are off now
            if timeNow - self.timeTurnedOff > self.secondsOff:
                # exceeded the OFF time, turn on
                self.bIsOn = True
                self.timeTurnedOff = timeNow
                justSwitched = True

        return (self.bIsOn, justSwitched)


if __name__ == '__main__':
    print 'hello'

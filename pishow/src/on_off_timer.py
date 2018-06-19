#!/usr/bin/env python3
"""on_off_timer.py - alternates  on/off state for specific on/off durations"""

import time


class OnOffTimer(object):
    """Alternate between ON and OFF states for specific On/Off durations"""

    def __init__(self, on_duration, off_duration, startOn=False):
        """constructor"""
        self.on_duration = on_duration
        self.off_duration = off_duration
        self._is_on = startOn
        now = time.time()
        if startOn:
            self.turn_on_time = now
            self.turn_off_time = None
        else:
            self.turn_on_time = None
            self.turn_off_time = now

    def is_on(self):
        """
        Returns whether we are on or not right now (first return value of pair),
        but it also returns whether we have just switched state from ON to OFF
        or vice versa.
        """
        now = time.time()
        just_switched = False
        if self._is_on:
            # we are on now
            if now - self.turn_on_time > self.on_duration:
                # exceeded the ON time, turn off
                self._is_on = False
                self.turn_off_time = now
                just_switched = True
        else:
            # we are off now
            if now - self.turn_off_time > self.off_duration:
                # exceeded the OFF time, turn on
                self._is_on = True
                self.turn_on_time = now
                just_switched = True

        return (self._is_on, just_switched)

    def is_off(self):
        """trivial"""
        return not self.is_on()


# unit test:
if __name__ == "__main__":
    TIMER = OnOffTimer(.33, .67, True)
    COUNT = 0
    while COUNT < 42:
        print(TIMER.is_on())
        time.sleep(.05)
        COUNT += 1

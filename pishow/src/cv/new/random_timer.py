#!/usr/bin/env python3
"""random_timer.py - like pins-based wall-mounted timers, with randomness"""

import time


class RandomTimer(object):
    """like pins-based wall-mounted timers, with randomness"""

    def __init__(self, minOn, maxOn, minOff, maxOff):
        """constructor"""
        self.minOn = minOn
        self.maxOn = maxOn

        self.minOff = minOff
        self.maxOff = maxOff

        self.bPrevWasOn = False
        self.bIsOn = False

        self.update()

    def turn_on(self):
        """Switch to ON mode"""
        self.bIsOn = True

    def update(self):
        """Tracks last time is_on() or just_turned_on() is called"""
        self.lastUpdateTime = time.time()

    def is_on(self):
        """returns whether we are on or not right now"""
        self.update()
        return self.bIsOn

    def just_turned_on(self):
        """returns whether we are on AND last time we checked we were not on"""
        self.update()

if __name__ == '__main__':
    print('hello')

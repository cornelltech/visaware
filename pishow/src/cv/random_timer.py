#!/usr/bin/env python
"""random_timer.py - like pins-based wall-mounted timers, with randomness"""


class RandomTimer(object):
    """like pins-based wall-mounted timers, with randomness"""

    def __init__(self, minOn, maxOn, minOff, maxOff):
        """constructor"""
        self.minOn = minOn
        self.maxOn = maxOn

        self.minOff = minOff
        self.maxOff = maxOff

        self.bIsOn = False

    def update(self):

    def is_on(self):
        """returns whether we are on or not right now"""
        self.update()
        return self.bIsOn

    def just_turned_on(self):
        """returns whether we are on AND last time we checked we were not on"""
        self.update()

if __name__ == '__main__':
    print 'hello'

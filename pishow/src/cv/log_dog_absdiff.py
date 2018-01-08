#!/usr/bin/env python

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import cv2
import looper
import log_dog
import absdiff


class LogDogAbsDiff:
    """Log-Dog then AbsDiff"""

    def __init__(self):
        self.log_dog = log_dog.LogDog()
        self.absdiff = absdiff.AbsDiff()

    def apply(self, frame):
        """Log-Dog then AbsDiff"""
        return self.absdiff.apply(self.log_dog.apply(frame))


if __name__ == '__main__':
    (looper.parse_command_line(LogDogAbsDiff()))()
    cv2.destroyAllWindows()

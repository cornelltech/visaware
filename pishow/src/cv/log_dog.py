#!/usr/bin/env python
"""log_dog.py"""

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
# import looper
import looper_threaded
import numpy
import log


ON_SIZE = 3
OFF_SIZE = 155

class LogDog:
    """log-dog a frame"""

    def __init__(self):
        """constructor"""
        self.log = log.Log()

    def apply(self, frame):
        """log-dog a frame"""
        log_scaled = self.log.apply(frame)
        blur_on = cv2.GaussianBlur(log_scaled, (ON_SIZE, ON_SIZE), 0)
        blur_off = cv2.GaussianBlur(log_scaled, (OFF_SIZE, OFF_SIZE), 0)
        return blur_on-blur_off


if __name__ == '__main__':
    (looper_threaded.parse_command_line(LogDog()))()
    cv2.destroyAllWindows()

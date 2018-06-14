#!/usr/bin/env python
"""log.py"""

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
import looper
import numpy
import gray


LOG_FACTOR = 3

class Log:
    """log a frame"""

    def __init__(self):
        """constructor"""
        self.gray = gray.Gray()

    def apply(self, frame):
        """log a frame"""
        frame = self.gray.apply(frame)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(frame)
        log_scaled = numpy.log(1+LOG_FACTOR*(frame-min_val)/(max_val-min_val))
        return log_scaled


if __name__ == '__main__':
    (looper.parse_command_line(Log()))()
    cv2.destroyAllWindows()

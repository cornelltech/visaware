#!/usr/bin/env python
"""gray.py"""

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
import looper
import numpy


class Gray:
    """gray a frame"""

    def apply(self, frame):
        """gray frame"""
        if numpy.size(frame[0, 0]) == 3:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            return frame


if __name__ == '__main__':
    (looper.parse_command_line(Gray()))()
    cv2.destroyAllWindows()

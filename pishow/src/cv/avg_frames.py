#!/usr/bin/env python
"""avg_frames.py"""

import cv2
import looper
import gray
import numpy


# Check out Abid Rahman's blog here (almost the same idea):
# opencvpython.blogspot.com/2012/07/background-extraction-using-running.html
# NB: will get big errors after a while if don't normalize each frame

class AvgFrames:
    """average frames"""

    def __init__(self):
        """constructor"""
        self.alpha = 0.01
        self.frame = None

    def apply(self, frame):
        """returns avg of all frames after updating with weighted frame"""
        frame = numpy.float32(frame)
        if self.frame is None:
            self.frame = frame
        else:
            self.frame = cv2.accumulateWeighted(frame, self.frame, self.alpha)
        return cv2.convertScaleAbs(self.frame)


if __name__ == '__main__':
    (looper.parse_command_line(AvgFrames()))()
    cv2.destroyAllWindows()

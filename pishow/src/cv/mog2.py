#!/usr/bin/env python
"""mog2.py"""

import cv2
import looper
import gray


class Mog2:
    """Mog2 background subtraction"""

    def __init__(self):
        """constructor"""
        self.gray = gray.Gray()
        self.fgbg = cv2.createBackgroundSubtractorMOG2()


    def apply(self, frame):
        """Mog2 background subtraction"""
        return self.fgbg.apply(self.gray.apply(frame))


if __name__ == '__main__':
    (looper.parse_command_line(Mog2()))()
    cv2.destroyAllWindows()

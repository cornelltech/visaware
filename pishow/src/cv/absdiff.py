#!/usr/bin/env python3
"""absdiff.py"""

import cv2
import looper
import gray
import numpy


class AbsDiff:
    """absolute value of (current_frame - previous_frame)"""

    def __init__(self):
        """constructor"""
        self.gray = gray.Gray()
        self.last_frame = None

    def apply(self, frame):
        """returns diff"""
        frame = self.gray.apply(frame)
        if self.last_frame is None:
            self.last_frame = frame
            return frame
        else:
            result = cv2.absdiff(frame, self.last_frame)
            self.last_frame = frame
            return result


if __name__ == '__main__':
    (looper.parse_command_line(AbsDiff()))()
    cv2.destroyAllWindows()

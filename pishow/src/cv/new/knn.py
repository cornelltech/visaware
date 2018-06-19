#!/usr/bin/env python3
"""knn.py"""

import cv2
import looper
import gray


class KNN:
    """KNN background subtraction"""

    def __init__(self):
        """constructor"""
        self.gray = gray.Gray()
        self.fgbg = cv2.createBackgroundSubtractorKNN(10, 500.0, False)


    def apply(self, frame):
        """KNN background subtraction"""
        return self.fgbg.apply(self.gray.apply(frame))


if __name__ == '__main__':
    (looper.parse_command_line(KNN()))()
    cv2.destroyAllWindows()

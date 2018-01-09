#!/usr/bin/env python
"""avg_n_frames.py"""

import cv2
import looper
import gray
import numpy


class AvgNFrames:
    """average n frames"""

    def __init__(self):
        """constructor"""
        self.n_frames = 10
        self.frames = []
        self.avg_frame = None

    def apply(self, frame):
        """returns average of self.n_frames frames after updating w/frame"""
        frame = numpy.float32(frame)
        self.frames.insert(0, frame)
        if self.avg_frame is None:
            self.avg_frame = frame
        elif len(self.frames) < self.n_frames:
            self.avg_frame = self.avg_frame + frame
        else:
            self.avg_frame = self.avg_frame - self.frames.pop() + frame
        return cv2.convertScaleAbs(self.avg_frame/float(len(self.frames)))


if __name__ == '__main__':
    (looper.parse_command_line(AbsDiff()))()
    cv2.destroyAllWindows()

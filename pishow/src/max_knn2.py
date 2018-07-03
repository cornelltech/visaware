#!/usr/bin/env python3
"""knn.py"""

import time
import sys
import cv2
from gray import Gray


# a silhouette can not have MORE than this number of pixels
NO_MORE_THAN = 30000
# a silhouette can not have LESS than this number of pixels
NO_LESS_THAN = 10000
# a silhouette cannot be closer than INNER_MARGIN pixels from the border
INNER_MARGIN = 10

# KNN background subtractor history param
KNN_HISTORY = 10
# KNN background subtractor threshold param
KNN_THRESH = 500.0

# Min # of nonzero pixels for us to believe there's motion
MOTION_MIN_NNZ = 100

# how long do we wait before we start timing things?
IDLE_START_TIME = 0.5

class MaxKNN(Gray):
    """KNN background subtraction"""
    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.fgbg = cv2.createBackgroundSubtractorKNN(
            KNN_HISTORY, KNN_THRESH, False)
        self.start_time = time.time()
        self.moving = False
        self.max_nnz = 0
        self.max_i = 0
        self.max_img = None
        self.i_frame = 0

    def process_frame(self, frame):
        """KNN background subtraction"""
        gray = super().process_frame(frame)
        knn_img = self.fgbg.apply(gray)
        nnz = cv2.countNonZero(knn_img)

        if time.time() - self.start_time < IDLE_START_TIME:
            # Do nothing for the first IDLE_START_TIME seconds
            time.sleep(IDLE_START_TIME/10.0)
            return knn_img

        if nnz > MOTION_MIN_NNZ:
            if not self.moving:
                print('Motion turns ON')
                self.moving = True
        else:
            if self.moving:
                print('Motion turns OFF')
                self.moving = False
                self.reset()

    def reset(self):
        

        return knn_img


if __name__ == '__main__':
    MaxKNN(sys.argv[1]).start()

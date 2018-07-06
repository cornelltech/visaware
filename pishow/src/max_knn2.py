#!/usr/bin/env python3
"""knn.py"""

import time
import sys
import cv2
import numpy as np
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
        self.disp_img = None

    def reset(self, frame):
        """Re-sets self.disp_img"""
        if self.disp_img is None:
            self.disp_img = np.zeros(frame.shape)

    def process_frame(self, frame):
        """KNN background subtraction"""
        gray = super().process_frame(frame)
        knn_img = self.fgbg.apply(gray)
        nnz = cv2.countNonZero(knn_img)

        frame_shape = frame.shape
        img_h = frame_shape[0]
        img_w = frame_shape[1]

        if self.disp_img is None:
            self.disp_img = np.zeros((img_h, img_w))

        rect = cv2.boundingRect(knn_img)
        bb_x, bb_y, bb_w, bb_h = rect

        if nnz > self.max_nnz and \
           nnz < NO_MORE_THAN and \
           nnz > NO_LESS_THAN and \
           bb_x > INNER_MARGIN and \
           bb_x + bb_w < img_w - INNER_MARGIN:

            print('- found next candidate: ', self.grabbed_frame_num())
            # found the next candidate silhouette to use
            self.max_nnz = nnz
            
            # crop rect into max_img
            # self.max_img = knn_img.copy()
            self.max_img = knn_img[bb_y:bb_y + bb_h, bb_x:bb_x+bb_w]

        if time.time() - self.start_time < IDLE_START_TIME:
            # Do nothing for the first IDLE_START_TIME seconds
            time.sleep(IDLE_START_TIME/10.0)
            return knn_img

        if nnz > MOTION_MIN_NNZ:
            if not self.moving:
                print('Motion turns ON')
                self.moving = True
                self.max_nnz = 0
        else:
            if self.moving:
                print('Motion turns OFF')
                self.moving = False
                # self.disp_img = self.max_img
                rows, cols = self.max_img.shape
                self.disp_img[10:10+rows, 10:10+cols] = self.max_img

        return self.disp_img


if __name__ == '__main__':
    MaxKNN(sys.argv[1]).start()

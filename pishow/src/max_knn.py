#!/usr/bin/env python3
"""knn.py"""

import sys
import cv2
from gray import Gray


# a silhouette can not have MORE than this number of pixels
NO_MORE_THAN = 30000
# a silhouette can not have LESS than this number of pixels
NO_LESS_THAN = 10000
# a silhouette cannot be closer than INNER_MARGIN pixels from the border
INNER_MARGIN = 10


class MaxKNN(Gray):
    """KNN background subtraction"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.fgbg = cv2.createBackgroundSubtractorKNN(10, 500.0, False)
        self.max_nnz = 0
        self.max_i = 0
        self.max_img = None
        self.i_frame = 0

    def process_frame(self, frame):
        """KNN background subtraction"""
        gray = super().process_frame(frame)
        knn_img = self.fgbg.apply(gray)
        nnz = cv2.countNonZero(knn_img)

        img_h, img_w = knn_img.shape
        bb_x, bb_y, bb_w, bb_h = cv2.boundingRect(knn_img)

        bb_left = bb_x
        bb_right = bb_x + bb_w

        if nnz > self.max_nnz and nnz < NO_MORE_THAN and nnz > NO_LESS_THAN \
           and bb_left > INNER_MARGIN and bb_right < img_w - INNER_MARGIN:
            # found the next candidate silhouette to use
            self.max_nnz = nnz
            self.max_i = self.i_frame
            self.max_img = knn_img.copy()

        print('i: ', self.i_frame, '/ nnz: ', nnz, '/ max_i: ', self.max_i)

        self.i_frame += 1

        return knn_img

    def __del__(self):
        print('/ max_i: ', self.max_i)
        # cv2.imshow('max_img', self.max_img)
        cv2.imwrite('max.png', self.max_img)
        # cv2.waitKey(0)


if __name__ == '__main__':
    MaxKNN(cv2.VideoCapture(sys.argv[1])).start()

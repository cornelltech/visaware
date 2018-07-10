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

# vertical margin for drawing
HEIGHT_MARGIN = 100

# if TIME_DECAY_FACTOR < 1.0, the image values are less bright by this fraction
# if TIME_DECAY_FACTOR == 1.0, the image decays completely on every frame
TIME_DECAY_FACTOR = 0.0005

# how much to decay all other people by (i.e. to multiply them by
# PERSON_DECAY_FACTOR) when a new person comes into the picture
PERSON_DECAY_FACTOR = 0.8

# number of pixels to translate to the right each time
HORIZONTAL_TRANSLATION = 30

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
        self.subimg = None
        self.i_frame = 0
        self.disp_img = None
        self.start_x = 0
        self.last_time = time.time()

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

            # print('- found next candidate: ', self.grabbed_frame_num())
            # found the next candidate silhouette to use
            self.max_nnz = nnz

            # crop rect into max_img
            # self.subimg = knn_img.copy()
            self.subimg = cv2.convertScaleAbs(
                knn_img[bb_y:bb_y + bb_h, bb_x:bb_x+bb_w]
            )

        if time.time() - self.start_time < IDLE_START_TIME:
            # Do nothing for the first IDLE_START_TIME seconds
            time.sleep(IDLE_START_TIME / 10.0)
            return knn_img

        if nnz > MOTION_MIN_NNZ:
            if not self.moving:
                print('Motion turns ON')
                self.moving = True
                self.max_nnz = 0
        elif self.moving:
           now = time.time()
           delta_time = now - self.last_time
           self.last_time = now

           print('Motion turns OFF ', delta_time)

           self.moving = False

           self.disp_img, self.start_x = self.draw_silhouette(
               self.disp_img,
               self.subimg,
               self.start_x
           )

        self.disp_img = (1.0 - TIME_DECAY_FACTOR) * self.disp_img

        return cv2.convertScaleAbs(self.disp_img)

    def draw_silhouette(self, img, subimg, start_x):
        """draw_silhouette"""
        print('draw_silhouette(img, subimg, start_x=%d)' % start_x);

        img_height, img_width = img.shape[:2]

        subimg_height, subimg_width = subimg.shape[:2]

        # horizontal_translation = np.floor(0.5 * subimg_width)
        horizontal_translation = HORIZONTAL_TRANSLATION

        desired_subimg_height = img_height - 2 * HEIGHT_MARGIN

        if desired_subimg_height != subimg_height:
            factor = desired_subimg_height / subimg_height
            print('resizing height from %d to %d, factor: %f' %
                  (subimg_height, desired_subimg_height, factor))
            subimg = cv2.resize(subimg, (0, 0), fx=factor, fy=factor)
            subimg_height, subimg_width = subimg.shape[:2]

        end_x = start_x + subimg_width
        start_y = HEIGHT_MARGIN
        end_y = HEIGHT_MARGIN + subimg_height

        delta_x = end_x - img_width
        # check and fix for special case (which ends up being the main case
        # once we reach it) where you've reached the right end of the image
        if delta_x > 0:
            print('SURPASSED: DRAWING SUBIMG AT RHS END')
            # shift img to left first
            translation_mat = np.float32([[1, 0, -delta_x], [0, 1, 0]])
            img = cv2.warpAffine(img, translation_mat, (img_width, img_height))
            # also modify start_x and end_x for smaller subimg
            start_x = img_width - subimg_width
            end_x = img_width

        img = img * PERSON_DECAY_FACTOR

        # grab the subwindow we will partially overwrite from the image
        prev_subimg = img[start_y:end_y, start_x:end_x]

        # mask has nonzero pixels of subimg
        mask = subimg != 0

        prev_subimg[mask] = subimg[mask]

        # cv2.imshow('prev_subimg', prev_subimg)

        img[start_y:end_y, start_x:end_x] = prev_subimg

        return cv2.convertScaleAbs(img), start_x + horizontal_translation

if __name__ == '__main__':
    MaxKNN(sys.argv[1]).start()

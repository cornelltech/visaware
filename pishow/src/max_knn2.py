#!/usr/bin/env python3
"""knn.py"""

import time
import sys
import cv2
import numpy as np
from gray import Gray


# same as avg_frames.py ALPHA
ALPHA = 0.1

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

# the maximum time (between successive motion sequences) 
# anything longer than that would make the (prev) image 100% faded
MAX_TIME_FADE = 10

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
            self.subimg = knn_img[bb_y:bb_y + bb_h, bb_x:bb_x+bb_w]

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

                now = time.time()
                delta_time = now - self.last_time
                self.last_time = now

                print('Motion turns OFF ', delta_time)
                
                self.moving = False

                # before drawing new silhouette, fade self.disp_img by
                # how much time has passed since last motion detection
                scale_factor = 0.0
                if delta_time < MAX_TIME_FADE:
                    scale_factor = (MAX_TIME_FADE - delta_time) / MAX_TIME_FADE

                min, max, min_loc, max_loc = cv2.minMaxLoc(self.disp_img)
                
                self.disp_img = (self.disp_img - min) / (max - min)

                self.disp_img = np.float32(self.disp_img) * scale_factor

                # rows, cols = self.subimg.shape
                # self.disp_img[10:10+rows, 10:10+cols] = self.subimg
                self.disp_img, self.start_x = self.draw_silhouette(
                    self.disp_img,
                    self.subimg,
                    self.start_x
                )

        return self.disp_img

    def draw_silhouette(self, img, subimg, start_x):
        """draw_silhouette"""
        print('draw_silhouette(img, subimg, %d)' % start_x);
        print('self.start_x: %d' % self.start_x)

        img_shape = img.shape
        img_height = img_shape[0]
        img_width = img_shape[1]

        subimg_shape = subimg.shape
        subimg_height = subimg_shape[0]
        subimg_width = subimg_shape[1]
        half_subimg_width = np.floor(0.5 * subimg_width)

        desired_subimg_height = img_height - 2 * HEIGHT_MARGIN
        if desired_subimg_height != subimg_height:
            subimg_width = int(
                desired_subimg_height * subimg_width / subimg_height)
            subimg_height = int(desired_subimg_height)
            subimg = cv2.resize(subimg, (subimg_width, subimg_height))

        end_x = start_x + subimg_width
        end_y = HEIGHT_MARGIN + subimg_height
        start_y = HEIGHT_MARGIN

        delta_x = end_x - img_width
        if delta_x > 0:
            print('SURPASSED: DRAWING SUBIMG AT RHS END')

            start_x = img_width - subimg_width
            end_x = img_width

            # shift img to left first
            translation_matrix = np.float32([[1, 0, -delta_x], [0, 1, 0]])
            img = cv2.warpAffine(img, translation_matrix, 
                                 (img_width, img_height))
            img[start_y:end_y, start_x:end_x] = subimg
        else:
            img[start_y:end_y, start_x:end_x] = subimg
            
        next_start_x = int(start_x + half_subimg_width)
        return img, next_start_x


if __name__ == '__main__':
    MaxKNN(sys.argv[1]).start()

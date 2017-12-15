#!/usr/bin/env python

# this one works on a smaller image, also blurs it a bit before differencing
# this is smoother (less salt and pepper noise) and perhaps faster due to the
# smaller size.  more importantly this is less sensitive to camera color space
# fluctuations

import math
import cv2
import pishow
import numpy

BLUR_SIZE = 11
RESIZE_FACTOR = 0.5
FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
    gray_blurred = cv2.GaussianBlur(gray_small, (BLUR_SIZE, BLUR_SIZE), 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
    gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
    return FGBG.apply(255*gray_blurred)


if __name__ == '__main__':
    pishow.main_loop(callback)

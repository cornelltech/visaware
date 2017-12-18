#!/usr/bin/env python

# this version is like pishow-mog2-03.py BUT we subsample before doing anything
# else.  It seems to be slightly more sensitive than *03.py.

import math
import cv2
import pishow
import numpy

BLUR_SIZE = 11
RESIZE_FACTOR = 0.5
FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    small = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
    gray_small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray_small, (BLUR_SIZE, BLUR_SIZE), 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
    gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
    # mask = FGBG.apply(255*gray_blurred)
    return FGBG.apply(255*gray_blurred)

if __name__ == '__main__':
    pishow.main_loop(callback)

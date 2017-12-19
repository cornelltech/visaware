#!/usr/bin/env python

# same as 07 but showing mask only

import math
import cv2
import pishow
import numpy

BLUR_SIZE = 11
RESIZE_FACTOR = 0.5
FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    blurred = cv2.GaussianBlur(frame, (BLUR_SIZE, BLUR_SIZE), 0)
    gray_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
    gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
    mask = FGBG.apply(255*gray_blurred)
    return mask

if __name__ == '__main__':
    pishow.main_loop(callback)

#!/usr/bin/env python

# this one works on a smaller image, also blurs it a bit before differencing
# this is smoother (less salt and pepper noise) and perhaps faster due to the
# smaller size.  more importantly this is less sensitive to camera color space
# fluctuations

import math
import cv2
import looper
import numpy

BLUR_SIZE = 11
RESIZE_FACTOR = 0.5
FGBG = cv2.createBackgroundSubtractorMOG2()

# def callback(frame):
#     small = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
#     gray_small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
#     gray_blurred = cv2.GaussianBlur(gray_small, (BLUR_SIZE, BLUR_SIZE), 0)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
#     gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
#     proc = FGBG.apply(255*gray_blurred)
#     return cv2.resize(proc, (0, 0), fx=2.0, fy=2.0)

# def callback(frame):
#     blurred = cv2.GaussianBlur(frame, (BLUR_SIZE, BLUR_SIZE), 0)
#     gray_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
#     gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
#     mask = FGBG.apply(255*gray_blurred)
#     return mask

def callback(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_small = cv2.resize(gray, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
    gray_blurred = cv2.GaussianBlur(gray_small, (BLUR_SIZE, BLUR_SIZE), 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_blurred)
    gray_blurred = (gray_blurred-min_val)/(max_val-min_val)
    proc = FGBG.apply(255*gray_blurred)
    return cv2.resize(proc, (0, 0), fx=2.0, fy=2.0)


if __name__ == '__main__':
    (looper.parse_command_line(callback))()
    cv2.destroyAllWindows()

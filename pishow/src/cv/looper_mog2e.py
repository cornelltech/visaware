#!/usr/bin/env python

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
import looper
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
    neg_mask = cv2.bitwise_not(mask)
    bgimg = cv2.bitwise_and(frame, frame, mask = neg_mask)
    fgimg = cv2.bitwise_and(blurred, blurred, mask = mask) 
    # return cv2.bitwise_or(bgimg, fgimg)
    # return cv2.add(bgimg, fgimg)
    # return cv2.bitwise_or(fgimg, bgimg)
    return cv2.addWeighted(fgimg, 0.5, bgimg, 0.5, 0)


if __name__ == '__main__':
    (looper.parse_command_line(callback))()
    cv2.destroyAllWindows()

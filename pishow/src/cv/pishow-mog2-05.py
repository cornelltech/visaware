#!/usr/bin/env python

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
import pishow
import numpy

BLUR_SIZE = 11
RESIZE_FACTOR = 0.5

def callback(frame):
    small = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
    small_blurred = cv2.GaussianBlur(small, (BLUR_SIZE, BLUR_SIZE), 0)
    gray_small = small_blurred
    return gray_small

if __name__ == '__main__':
    pishow.main_loop(callback)

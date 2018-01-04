#!/usr/bin/env python

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import math
import cv2
import pishow
import numpy


LOG_FACTOR = 10
ON_SIZE = 3
OFF_SIZE = 11

FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)

    log_scaled = numpy.log(1+LOG_FACTOR*(gray-min_val)/(max_val-min_val))

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(log_scaled) 

    blur_on = cv2.GaussianBlur(log_scaled, (ON_SIZE, ON_SIZE), 0)
    blur_off = cv2.GaussianBlur(log_scaled, (OFF_SIZE, OFF_SIZE), 0)    

    dog = blur_on-blur_off
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(log_scaled) 
    dog = 255*(dog-min_val)/(max_val-min_val)

    return FGBG.apply(dog)

if __name__ == '__main__':
    pishow.main_loop(callback)
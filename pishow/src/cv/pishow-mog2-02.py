#!/usr/bin/env python

# an attempt to make the MOG2 result more stable with bad camera

import cv2
import pishow

FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    proc = FGBG.apply(small)
    return cv2.resize(proc, (640, 480))
    
if __name__ == '__main__':
    pishow.main_loop(callback)

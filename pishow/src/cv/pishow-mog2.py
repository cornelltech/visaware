#!/usr/bin/env python

import cv2
import pishow

FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    return FGBG.apply(frame)
    
if __name__ == '__main__':
    pishow.main_loop(callback)

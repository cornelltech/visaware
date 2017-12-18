#!/usr/bin/env python

# show stream in half size

import cv2
import pishow

RESIZE_FACTOR = 0.5

def callback(frame):
    half_size = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
    return half_size

if __name__ == '__main__':
    pishow.main_loop(callback)

#!/usr/bin/env python

import cv2
import looper

FGBG = cv2.createBackgroundSubtractorKNN()

def callback(frame):
    return FGBG.apply(frame)
    

if __name__ == '__main__':
    (looper.parse_command_line(callback))()
    cv2.destroyAllWindows()

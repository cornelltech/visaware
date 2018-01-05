#!/usr/bin/env python

# same as looper_mog2.py but done at half res (displayed at full res)

import cv2
import looper

FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    proc = FGBG.apply(small)
    return cv2.resize(proc, (0, 0), fx=2.0, fy=2.0)


if __name__ == '__main__':
    (looper.parse_command_line(callback))()
    cv2.destroyAllWindows()

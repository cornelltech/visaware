#!/usr/bin/env python

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import cv2
import looper
import log_dog


FGBG = cv2.createBackgroundSubtractorMOG2()

def callback(frame):
    log_dog_result = log_dog.callback(frame)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(log_dog_result)
    log_dog_rescaled = 255.0*(log_dog_result-min_val)/(max_val-min_val)
    return FGBG.apply(log_dog_rescaled)


if __name__ == '__main__':
    (looper.parse_command_line(callback))()
    cv2.destroyAllWindows()

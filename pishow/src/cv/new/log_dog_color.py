#!/usr/bin/env python3
"""log_dog_color.py"""

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import cv2
import looper
import numpy
import log_dog


class LogDogColor:
    """log-dog a frame, show in color"""

    def __init__(self):
        """constructor"""
        self.log_dog = log_dog.LogDog()

    def apply(self, frame):
        """log-dog a frame"""
        lab_img = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        (l_img, a_img, b_img) = cv2.split(lab_img)
        l_img = self.log_dog.apply(frame)
        l_img = numpy.floor(128.0+(128.0*l_img)).astype('uint8')
        lab_img = cv2.merge([l_img, a_img, b_img])
        return cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)


if __name__ == '__main__':
    (looper.parse_command_line(LogDogColor()))()
    cv2.destroyAllWindows()

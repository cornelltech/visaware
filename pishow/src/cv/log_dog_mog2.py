#!/usr/bin/env python
"""log_dog_mog2.py"""

# this one's just here to show what the original (subsampled) looks like when
# blurred -- we want to make sure people cannot be identified when this one
# shows

import cv2
import looper
import log_dog
import mog2


LOG_DOG_SCALE_FACTOR = 50

class LogDogMog2:
    """Log-Dog then Mog2"""

    def __init__(self):
        self.log_dog = log_dog.LogDog()
        self.mog2 = mog2.Mog2()

    def apply(self, frame):
        """Log-Dog then Mog2"""
        return self.mog2.apply(
            128.0+ self.log_dog.apply(frame)*LOG_DOG_SCALE_FACTOR)


if __name__ == '__main__':
    (looper.parse_command_line(LogDogMog2()))()
    cv2.destroyAllWindows()

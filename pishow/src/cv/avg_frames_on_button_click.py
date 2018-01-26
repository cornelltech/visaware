#!/usr/bin/env python
"""avg_frames.py"""

import cv2
import looper
import avg_frames
import numpy
import RPi.GPIO as GPIO

GPIO_PIN = 18

class AvgFramesOnButton:
    """average frames"""

    def __init__(self):
        """constructor"""
        self.avgFrames = avg_frames.AvgFrames()
        self.noActivityFrame = None
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def apply(self, frame):
        """returns avg of all frames after updating with weighted frame"""
        frame = self.avgFrames.apply(frame)

        # if self.noActivityFrame is None and frame is not None:
        if self.noActivityFrame is None:
            # initialize blank (no activity) frame if haven't done so already
            self.noActivityFrame = numpy.zeros(frame.shape)

        print GPIO.input(GPIO_PIN)

        return frame


if __name__ == '__main__':
    (looper.parse_command_line(AvgFramesOnButton()))()
    cv2.destroyAllWindows()

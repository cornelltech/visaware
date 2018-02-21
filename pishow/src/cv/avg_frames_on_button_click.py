#!/usr/bin/env python
"""avg_frames.py"""

import datetime
import time
import sys
import cv2
import looper
import avg_frames
import numpy
import RPi.GPIO as GPIO
import socket


GPIO_PIN = 18

class AvgFramesOnButton:
    """average frames"""

    def __init__(self):
        """constructor"""
        self.avgFrames = avg_frames.AvgFrames()
        self.noActivityFrame = None
        self.lastGpioState = None
        if socket.gethostname() == "pishow-150":
            self.fullscreenSize = (1280, 1024)
        else:
            self.fullscreenSize = (1280, 1024)
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def apply(self, frame):
        """returns avg of all frames after updating with weighted frame"""
        # if self.noActivityFrame is None and frame is not None:
        if self.noActivityFrame is None:
            # initialize blank (no activity) frame if haven't done so already
            # (this only happens once at the start)
            self.noActivityFrame = numpy.zeros(frame.shape)

        gpioState = GPIO.input(GPIO_PIN)

        if self.lastGpioState != gpioState:
            print '%s\t%s' % (datetime.datetime.now(), gpioState)
            sys.stdout.flush()

        if gpioState == 1:
            # ENGAGED: button is pressed down
            frame = self.noActivityFrame
        else:
            # DISENGAGED: button is not pressed
            frame = self.avgFrames.apply(frame)

        # time.sleep(0.1)

        self.lastGpioState = gpioState

        return cv2.resize(frame, self.fullscreenSize)


if __name__ == '__main__':
    (looper.parse_command_line(AvgFramesOnButton()))()
    cv2.destroyAllWindows()

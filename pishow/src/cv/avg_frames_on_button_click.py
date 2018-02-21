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
import on_off_timer


GPIO_PIN = 18
# timer on state duration
ON_SECONDS = 120
# timer off state duration
OFF_SECONDS = 900

class AvgFramesOnButton:
    """average frames"""

    def __init__(self):
        """constructor"""
        self.timer = on_off_timer.OnOffTimer(ON_SECONDS, OFF_SECONDS)
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

        timeNow = datetime.datetime.now()

        if self.lastGpioState != gpioState:
            print '%s\t%s' % (timeNow, gpioState)

        bTimerIsOn, bJustSwitched = self.timer.is_on()

        if bTimerIsOn:
            timerState = 'ON'
        else:
            timerState = 'OFF'

        if bJustSwitched:
            print '{}\tTimer: turning system {}'.format(
                timeNow, timerState)

        if gpioState == 1 and not bTimerIsOn:
            # DISENGAGED
            frame = self.noActivityFrame
        else:
            # ENGAGED
            frame = self.avgFrames.apply(frame)

        # time.sleep(0.1)

        self.lastGpioState = gpioState

        sys.stdout.flush()

        return cv2.resize(frame, self.fullscreenSize)


if __name__ == '__main__':
    (looper.parse_command_line(AvgFramesOnButton()))()
    cv2.destroyAllWindows()

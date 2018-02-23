#!/usr/bin/env python
"""avg_frames_on_button_click.py"""

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
from threading import Thread


################################################################################
# Socket (full-duplex) communication globals (code here is the server code)
################################################################################

# One pishow (this one) is the socket server, the other pishow is socket client.
CLIENT_PISHOW_SOCKET_IP = "128.84.84.130"
SOCKET_PORT = 5005
SOCKET_MAX_QUEUED_CONNECTIONS = 5
# we only send one byte to indicate on or off
SOCKET_BUFFER_SIZE = 1

################################################################################
# GPIO globals
################################################################################
GPIO_PIN = 18

################################################################################
# TIMING globals
################################################################################
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
        hostname = socket.gethostname()
        if hostname == "pishow-150":
            self.fullscreenSize = (1280, 1024)
        else:
            self.fullscreenSize = (1280, 1024)

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.socket_thread_stopped = True
        self.last_socket_data = None
        self.last_socket_receive_time = None
        # start the socket listening
        self.start_socket_thread()

    def __del__(self):
        # stop via this variable
        self.socket_thread_stopped = True
        # make sure you give enough time for thread to see the variable change
        time.sleep(100)
        # TODO: there is probably a better way to stop

    def start_socket_thread(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", SOCKET_PORT))
        self.server_socket.listen(SOCKET_MAX_QUEUED_CONNECTIONS)
        self.socket_thread_stopped = False
        thread = Thread(target=self.socket_thread_worker, args=())
        thread.daemon = True
        thread.start()

    def socket_thread_worker(self):
        # while True:
        #     if self.socket_thread_stopped:
        #         return

        #     time.sleep(0.1)

        #     (client_socket, address) = self.server_socket.accept()
        #     # do something with client_socket: try to receive one byte
        #     data = client_socket.recv(1)
        #     print data
        #     self.last_socket_receive_time = time.time()
        #     self.last_socket_data = data
        pass

    def apply(self, frame):
        """returns avg of all frames after updating with weighted frame"""
        # if self.noActivityFrame is None and frame is not None:
        if self.noActivityFrame is None:
            # initialize blank (no activity) frame if haven"t done so already
            # (this only happens once at the start)
            self.noActivityFrame = numpy.zeros(frame.shape)

        gpioState = GPIO.input(GPIO_PIN)

        timeNow = datetime.datetime.now()

        if self.lastGpioState != gpioState:
            print "%s\t%s" % (timeNow, gpioState)

        # determine whether our timer module is currrently on or not
        # and whether it just switched states (since the last time we checked)
        bTimerIsOn, bJustSwitched = self.timer.is_on()

        if bTimerIsOn:
            timerState = "ON"
        else:
            timerState = "OFF"

        if bJustSwitched:
            print "{}\tTimer: turning system {}".format(
                timeNow, timerState)

        if gpioState == 1 and not bTimerIsOn and self.last_socket_data != 'a':
            # DISENGAGED
            frame = self.noActivityFrame
        else:
            # ENGAGED
            frame = self.avgFrames.apply(frame)

        # time.sleep(0.1)

        self.lastGpioState = gpioState

        sys.stdout.flush()

        return cv2.resize(frame, self.fullscreenSize)


if __name__ == "__main__":
    (looper.parse_command_line(AvgFramesOnButton()))()
    cv2.destroyAllWindows()

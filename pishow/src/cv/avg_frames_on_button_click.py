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
        self.avg_frames = avg_frames.AvgFrames()
        self.no_activity_frame = None
        self.last_gpio_state = None
        hostname = socket.gethostname()
        if hostname == "pishow-150":
            self.fullscreen_size = (1280, 1024)
            self.hostname_to_message = "pishow-130"
        else:
            self.fullscreen_size = (1280, 1024)
            self.hostname_to_message = "pishow-150"

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket = None
        self.server_socket_thread_stopped = True
        self.last_socket_data = None
        self.last_socket_receive_time = None
        # start the socket listening
        self.start_server_socket_thread()

    def __del__(self):
        # stop via this variable
        self.server_socket_thread_stopped = True
        # make sure you give enough time for thread to see the variable change
        time.sleep(100)
        # TODO: there is probably a better way to stop

    def start_server_socket_thread(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", SOCKET_PORT))
        self.server_socket.listen(SOCKET_MAX_QUEUED_CONNECTIONS)
        self.server_socket_thread_stopped = False
        thread = Thread(target=self.server_socket_thread_worker, args=())
        thread.daemon = True
        thread.start()

    def server_socket_thread_worker(self):
        while True:
            if self.server_socket_thread_stopped:
                return

            time.sleep(0.1)

            (my_clients_socket, address) = self.server_socket.accept()
            # do something with client_socket: try to receive one byte
            data = my_clients_socket.recv(1)
            self.last_socket_receive_time = time.time()
            self.last_socket_data = data

    def tell_other_i_just_turned_on(self):
        self.client_socket.connect((self.hostname_to_message, SOCKET_PORT))
        self.client_socket.send('1')
        self.client_socket.close()

    def apply(self, frame):
        """returns avg of all frames after updating with weighted frame"""
        # if self.no_activity_frame is None and frame is not None:
        if self.no_activity_frame is None:
            # initialize blank (no activity) frame if haven"t done so already
            # (this only happens once at the start)
            self.no_activity_frame = numpy.zeros(frame.shape)

        gpio_state = GPIO.input(GPIO_PIN)

        timeNow = datetime.datetime.now()

        if self.last_gpio_state != gpio_state:
            # we have changed GPIO state - toggled the switch just now
            # either we changed from on to off or vice versa
            print "[1] last data: %s" % self.last_socket_data
            print "%s\t%s" % (timeNow, gpio_state)
            
            # only in the case of having just turned on (gpio__state == 0)
            # do we tell the other board, because in that case we want the
            # other board to turn on too
            self.tell_other_i_just_turned_on()

        # determine whether our timer module is currrently on or not
        # and whether it just switched states (since the last time we checked)
        bTimerIsOn, bJustSwitched = self.timer.is_on()

        if bTimerIsOn:
            timerState = "ON"
        else:
            timerState = "OFF"

        if bJustSwitched:
            print "[2] last data: %s" % self.last_socket_data
            print "{}\tTimer: turning system {}".format(
                timeNow, timerState)

        if gpio_state == 1 and not bTimerIsOn:
            # DISENGAGED
            frame = self.no_activity_frame
        else:
            # ENGAGED
            frame = self.avg_frames.apply(frame)

        # time.sleep(0.1)

        self.last_gpio_state = gpio_state

        sys.stdout.flush()

        return cv2.resize(frame, self.fullscreen_size)


if __name__ == "__main__":
    (looper.parse_command_line(AvgFramesOnButton()))()
    cv2.destroyAllWindows()

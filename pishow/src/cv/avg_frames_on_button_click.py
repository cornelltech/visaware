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
SOCKET_PORT = 5005
SOCKET_MAX_QUEUED_CONNECTIONS = 5
# we only send one byte to indicate on or off
SOCKET_BUFFER_SIZE = 1
# the number of seconds after receiving a message from the other board
# (telling us that it just turned on) during which we will turn on this
# board's showing machinery. i.e. we display with this board if the other
# board has sent a message less than SOCKET_RECEIVE_TIME_THRESHOLD
# seconds. This keeps projection on this board in "on" state for at least
# (SOCKET_RECEIVE_TIME_THRESHOLD seconds) time.
SOCKET_RECEIVE_TIME_THRESHOLD = 60.0

################################################################################
# GPIO globals
################################################################################
GPIO_PIN = 18

################################################################################
# TIMER-related globals
################################################################################
# timer on state duration
TIMER_ON_SECONDS = 120
# timer off state duration
TIMER_OFF_SECONDS = 3480

################################################################################
# Time-related globals
################################################################################

MIN_SECONDS_ON = 60

class AvgFramesOnButton:
    """average frames"""

    def __init__(self):
        """constructor"""
        self.timer = on_off_timer.OnOffTimer(TIMER_ON_SECONDS,
                                             TIMER_OFF_SECONDS)
        self.avg_frames = avg_frames.AvgFrames()
        self.no_activity_frame = None
        self.last_gpio_state = None

        if socket.gethostname() == "pishow-150":
            self.fullscreen_size = (1280, 1024)
            self.hostname_to_message = "pishow-130"
        else:
            self.fullscreen_size = (1280, 1024)
            self.hostname_to_message = "pishow-150"

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        print "tell_other_i_just_turned_on(self)"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.hostname_to_message, SOCKET_PORT))
            self.client_socket.send('1')
            self.client_socket.close()
        except:
            print "UNABLE TO SEND MESSAGE TO %s!" % self.hostname_to_message


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
        timer_is_on, just_switched = self.timer.is_on()

        if timer_is_on:
            timer_state = "ON"
        else:
            timer_state = "OFF"

        if just_switched:
            print "[2] last data: %s" % self.last_socket_data
            print "{}\tTimer: turning system {}".format(
                timeNow, timer_state)

        if self.last_socket_receive_time is not None:
            time_since_message_arrived = (time.time()-
                                          self.last_socket_receive_time)
        else:
            time_since_message_arrived = float('inf')

        received_on_message = (time_since_message_arrived <
                               SOCKET_RECEIVE_TIME_THRESHOLD)

        if( gpio_state == 1 and 
            not timer_is_on and 
            not received_on_message):
            # DISENGAGED
            frame = self.no_activity_frame
        else:
            # ENGAGED
            frame = self.avg_frames.apply(frame)

        # time.sleep(0.1)

        self.last_gpio_state = gpio_state

        sys.stdout.flush()

        return cv2.resize(frame, self.fullscreen_size)

    cv2.destroyAllWindows()

#!/usr/bin/env python3
"""avg_frames_on_button_click.py"""

import sys
import time
import socket
import requests
from threading import Thread, ThreadError
import RPi.GPIO as GPIO
import cv2
import numpy as np
from avg_frames import AvgFrames
from on_off_timer import OnOffTimer


################################################################################
# Visualization related globals
################################################################################

WINDOW_NAME = 'cam'

# path to image we show when there is no activity
SPLASH_IMAGE_PATH = '/home/pi/workspace/visaware/pishow/src/splash.jpg'

################################################################################
# Sockets-related globals
################################################################################

# One pishow (this one) is the socket server, the other pishow is socket client.
SOCKET_PORT = 5005
# we only send one byte at a time
SOCKET_BUFFER_SIZE = 1
# the number of seconds after receiving a message from the other board
# (telling us that it just turned on) during which we will turn on this
# board's showing machinery. i.e. we display with this board if the other
# board has sent a message less than SOCKET_RECEIVE_TIME_THRESHOLD
# seconds. This keeps projection on this board in "on" state for at least
# (SOCKET_RECEIVE_TIME_THRESHOLD seconds) time.
SOCKET_RECEIVE_TIME_THRESHOLD = 60.0
# how long to sleep between each time you listen to a socket
SOCKET_SERVER_THREAD_SLEEP = 0.1

################################################################################
# GPIO-related globals
################################################################################

GPIO_PIN = 18

################################################################################
# Time-related globals
################################################################################

# timer on-state duration
TIMER_ON_SECONDS = 120
# timer off-state duration
TIMER_OFF_SECONDS = 3480
# minimum duration to show the other side pisee
MIN_SECONDS_ON = 45

class AvgFramesOnButtonClick():
    """Show avg frames when switch is on, otherwise show splash screen"""
    def __init__(self, arguments):
        self.my_ip = arguments[1]
        self.other_ip = arguments[2]
        self.webcam_url = arguments[3]
        self.fullscreen_size = (int(arguments[4]), int(arguments[5]))

        cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

        self.no_activity_frame = cv2.imread(SPLASH_IMAGE_PATH)
        self.timer = OnOffTimer(TIMER_ON_SECONDS, TIMER_OFF_SECONDS)
        self.avg_frames = AvgFrames(None)
        self.state = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Start socket listening
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.last_socket_receive_time = None
        self.start_server_socket_thread()
        self.start_cam_thread()

    def start_cam_thread(self):
        self.stream = requests.get(self.webcam_url, stream=True)
        self.cam_thread_cancelled = False
        thread = Thread(target=self.cam_thread)
        thread.start()

    def cam_thread(self):
        bytes = b''
        while not self.cam_thread_cancelled:
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                       cv2.IMREAD_COLOR)

                    # here's where we process the frame
                    img = self.process_frame(img)

                    cv2.imshow(WINDOW_NAME, img)
                    if cv2.waitKey(1) ==27:
                        # exit(0)
                        self.shut_down()

            except ThreadError:
                self.cam_thread_cancelled = True

    def is_running(self):
        return self.cam_thread.isAlive()

    def shut_down(self):
        self.cam_thread_cancelled = True
        # block while waiting for thread to terminate
        while self.is_running():
            time.sleep(1)
        return True

    def start_server_socket_thread(self):
        """Start thread that listens on a socket"""
        try:
            self.server_socket.bind((self.my_ip, SOCKET_PORT))
        except OSError as os_error:
            print('Error: cannot bind to own IP. Are you sure %s is my IP?' %
                  self.my_ip)
            sys.exit(-1)
        thread = Thread(target=self.server_socket_thread_worker, args=())
        thread.daemon = True
        thread.start()

    def server_socket_thread_worker(self):
        """Socket listening thread main loop"""
        while True:
            bytes, address = self.server_socket.recvfrom(1)
            if bytes == b'1':
                print('received data: ', data, ', time: ', time.time())
                self.last_socket_receive_time = time.time()
            time.sleep(SOCKET_SERVER_THREAD_SLEEP)

    def tell_other_i_just_turned_on(self):
        """Send message telling other pishow that I've just started"""
        self.client_socket.sendto(b'1', (self.other_ip, SOCKET_PORT))
 
    def process_frame(self, frame):
        """Returns average of all frames after updating with weighted frame"""
        gpio_state = GPIO.input(GPIO_PIN)

        # determine whether our timer module is currrently on or not
        # and whether it just switched states (since the last time we checked)
        timer_is_on, just_switched = self.timer.is_on()

        if just_switched:
            print('Timer just switched state.')

        if self.last_socket_receive_time is not None:
            time_since_message_arrived = (time.time()-
                                          self.last_socket_receive_time)
        else:
            time_since_message_arrived = float('inf')

        received_on_message = (time_since_message_arrived <
                               SOCKET_RECEIVE_TIME_THRESHOLD)

        if gpio_state == 1 and not timer_is_on and not received_on_message:
            if self.state != 0:
                delta_time = time.time() - self.state
                if delta_time < MIN_SECONDS_ON:
                    frame = self.avg_frames.process_frame(frame)
                else:
                    print('DISENGAGE (DELTA_TIME > %ds)' % MIN_SECONDS_ON)
                    frame = self.no_activity_frame
                    self.state = 0
            else:

                frame = self.no_activity_frame
        else:
            frame = self.avg_frames.process_frame(frame)
            if self.state == 0:
                print('ENGAGE (STEPPED ON MAT)')
                self.tell_other_i_just_turned_on()
                # this ensures that only when we switch from state 0 to
                # an on state we will record self.state
                self.state = time.time()
        # sys.stdout.flush()
        return cv2.resize(frame, self.fullscreen_size)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    AvgFramesOnButtonClick(sys.argv).start()

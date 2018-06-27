#!/usr/bin/env python3
"""avg_frames_on_button_click.py"""

import sys
import time
import socket
from threading import Thread
import RPi.GPIO as GPIO
import cv2
from video_stream_abc import VideoStreamABC
from avg_frames import AvgFrames
from on_off_timer import OnOffTimer


################################################################################
# Networking globals
################################################################################

# NB: all communication is only between local and remote pishow boards

# At the Cornell Tech campus we have the following IP setup:

# pisee (near Benny's desk):  128.84.84.129
# pishow (near Benny's desk): 128.84.84.130
# pisee (CX lab):             128.84.84.149
# pishow (CX lab):            128.84.84.150

# IP number of (the other) pishow we are messaging.
HOST_IP_TO_MESSAGE = '128.84.84.150'

# URL of pisee (or ip-cam) camera stream
IP_CAM_URL = "http://128.84.84.149:8080/?action=stream"

################################################################################
# Visualization related globals
################################################################################

# resolution of the monitor or projector we are using
FULLSCREEN_SIZE = (1024, 768)
# path to image we show when there is no activity
SPLASH_IMAGE_PATH = '/home/pi/workspace/visaware/pishow/src/splash.jpg'

################################################################################
# Sockets-related globals
################################################################################

# One pishow (this one) is the socket server, the other pishow is socket client.
SOCKET_PORT = 5005
# 1 should be enough for SOCKET_MAX_QUEUED_CONNECTIONS - try it
SOCKET_MAX_QUEUED_CONNECTIONS = 5
# we only send one byte at a time
SOCKET_BUFFER_SIZE = 1
# the number of seconds after receiving a message from the other board
# (telling us that it just turned on) during which we will turn on this
# board's showing machinery. i.e. we display with this board if the other
# board has sent a message less than SOCKET_RECEIVE_TIME_THRESHOLD
# seconds. This keeps projection on this board in "on" state for at least
# (SOCKET_RECEIVE_TIME_THRESHOLD seconds) time.
SOCKET_RECEIVE_TIME_THRESHOLD = 60.0

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

def eprint(*args, **kwargs):
    """Same as print but goes to stderr"""
    print(*args, file=sys.stderr, **kwargs)

class AvgFramesOnButtonClick(VideoStreamABC):
    """Show avg frames when switch is on, otherwise show splash screen"""
    def __init__(self, stream):
        super().__init__(stream, full_screen=True)
        self.no_activity_frame = cv2.imread(SPLASH_IMAGE_PATH)
        self.timer = OnOffTimer(TIMER_ON_SECONDS, TIMER_OFF_SECONDS)
        self.avg_frames = AvgFrames(stream)
        self.state = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Start socket listening
        self.client_socket = None
        self.server_socket = None
        self.server_socket_thread_stopped = True
        self.last_socket_data = None
        self.last_socket_receive_time = None
        self.start_server_socket_thread()

    def start_server_socket_thread(self):
        """Start thread that listens on a socket"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", SOCKET_PORT))
        self.server_socket.listen(SOCKET_MAX_QUEUED_CONNECTIONS)
        self.server_socket_thread_stopped = False
        thread = Thread(target=self.server_socket_thread_worker, args=())
        thread.daemon = True
        thread.start()

    def server_socket_thread_worker(self):
        """Socket listening thread main loop"""
        while True:
            if self.server_socket_thread_stopped:
                return

            time.sleep(0.1)
            #pylint: disable=unused-variable
            (my_clients_socket, address) = self.server_socket.accept()
            #pylint: enable=unused-variable
            # do something with client_socket: try to receive one byte
            data = my_clients_socket.recv(1)
            self.last_socket_receive_time = time.time()
            self.last_socket_data = data

    def tell_other_i_just_turned_on(self):
        """Send message telling other pishow that I've just started"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((HOST_IP_TO_MESSAGE, SOCKET_PORT))
            self.client_socket.send(b'1')
            self.client_socket.close()
        except ConnectionRefusedError as err:
            eprint('Client Socket Error: Connection refused, cannot send msg.')
            eprint("Caught error: ", sys.exc_info()[0])
 
    def process_frame(self, frame):
        """Returns average of all frames after updating with weighted frame"""

        gpio_state = GPIO.input(GPIO_PIN)

        # determine whether our timer module is currrently on or not
        # and whether it just switched states (since the last time we checked)
        timer_is_on, just_switched = self.timer.is_on()

        if just_switched:
            print('Just switched!')

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
                    print('DISENGAGE (DELTA_TIME > %ds)' %
                          MIN_SECONDS_ON)
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

        # time.sleep(0.1)

        sys.stdout.flush()

        return cv2.resize(frame, FULLSCREEN_SIZE)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        AvgFramesOnButtonClick(cv2.VideoCapture(IP_CAM_URL)).start()
    # except IOError as (errno, strerror):
    #     print("IO Error ({0}): {1}".format(errno, strerror)
    # except ValueError, e:
    #     print("ValueError: {0}".format(e)
    except:
        print("Caught error: ", sys.exc_info()[0])

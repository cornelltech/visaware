#!/usr/bin/env python
"""looper.py"""

# Main loop and command line argument parsing and image display with FPS

import sys
import urllib
import time
import numpy
import cv2
from file_video_stream import FileVideoStream
from ip_video_stream import IpVideoStream
from webcam_video_stream import WebcamVideoStream

# constants for fps display overlayed on the (640px x 480px) image
FONT_LOCATION = (550, 460)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 64
FONT_LINE_TYPE = 2

# constant for buffer we hold image data in while streaming from url
BUFFER_LENGTH = 1024

def parse_command_line(effect):
    """Process command line arguments"""
    progname = sys.argv[0]
    usage_message = "Usage: %s [<url>|<file-path>]\n" % progname
    n_args = len(sys.argv)-1
    if n_args == 0:
        return lambda: loop_camera(effect)
    elif n_args == 1:
        arg = sys.argv[1]
        if arg == "-h" or arg == "--help":
            print usage_message
            sys.exit(0)
        elif arg[0:4] == "http":
            return lambda: loop_url(effect, arg)
        else:
            return lambda: loop_camera_or_file(effect, arg)
    else:
        print usage_message
        raise Exception("Only one argument allowed, you gave %d" % n_args)

def loop_camera(effect):
    """Loop camera"""
    print "loop_camera()"

def loop_file(effect, fileName):
    """Loop camera"""
    print "loop_file(%s)" % fileName

def loop_url(effect, url):
    """Loop url"""
    print "loop_url(\"%s\")" % url


if __name__ == "__main__":
    (parse_command_line(None))()
    cv2.destroyAllWindows()

#!/usr/bin/env python
"""looper.py"""

# Main loop and command line argument parsing and image display with FPS

import sys
import urllib
import time
import cv2
# from fps import FPS
# import file_video_stream as fvs
from ip_video_stream import IpVideoStream
from webcam_video_stream import WebcamVideoStream
from file_video_stream import FileVideoStream
from pacer import Pacer


# we run everything at a constant FPS for sanity, even if can do faster
NORMALIZED_FPS = 30

def parse_command_line(effect):
    """Process command line arguments"""
    progname = sys.argv[0]
    usage_message = "Usage: %s [<url>|<file-path>]\n" % progname
    n_args = len(sys.argv)-1
    if n_args == 0:
        return lambda: generic_looper(WebcamVideoStream().start(), effect)
    elif n_args == 1:
        arg = sys.argv[1]
        if arg == "-h" or arg == "--help":
            print usage_message
            sys.exit(0)
        elif arg[0:4] == "http":
            return lambda: generic_looper(IpVideoStream(arg).start(), effect)
        else:
            return lambda: generic_looper(
                FileVideoStream(arg, NORMALIZED_FPS).start(), effect)
    else:
        print usage_message
        raise Exception("Only one argument allowed, you gave %d" % n_args)


if __name__ == "__main__":
    (parse_command_line(None))()


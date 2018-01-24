#!/usr/bin/env python
"""looper.py"""

# Main loop and command line argument parsing and image display with FPS

import sys
import urllib
import time
import numpy
import cv2
from fps import FPS
from file_video_stream import FileVideoStream
from ip_video_stream import IpVideoStream
from webcam_video_stream import WebcamVideoStream
from pacer import Pacer

# we run everything at a constant FPS for sanity, even if can do faster
NORMALIZED_FPS = 30


def parse_command_line(effect):
    """Process command line arguments"""
    progname = sys.argv[0]
    usage_message = "Usage: %s [<url>|<file-path>]\n" % progname
    n_args = len(sys.argv)-1
    if n_args == 0:
        return lambda: loop_webcam(effect)
    elif n_args == 1:
        arg = sys.argv[1]
        if arg == "-h" or arg == "--help":
            print usage_message
            sys.exit(0)
        elif arg[0:4] == "http":
            return lambda: loop_url(effect, arg)
        else:
            return lambda: loop_file(effect, arg)
    else:
        print usage_message
        raise Exception("Only one argument allowed, you gave %d" % n_args)

def generic_looper(videoStream, effect):
    """same loop code for any stream"""
    fps = FPS().start()
    pacer = Pacer(NORMALIZED_FPS).start()

    while True:
        frame = videoStream.read()
        if frame is None:
            print 'frame is none!'
            break;
    
        if effect:
            frame = effect(frame)

        cv2.imshow('Frame', frame)
        fps.update()
        pacer.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # clean up at the end
    fps.stop()
    pacer.stop()
    videoStream.stop()

def loop_webcam(effect):
    """Loop webcam"""
    print "loop_webcam()"
    generic_looper(WebcamVideoStream().start(), effect)

def loop_file(effect, fileName):
    """Loop video file"""
    print "loop_file(%s)" % fileName
    generic_looper(FileVideoStream(fileName).start(), effect)

def loop_url(effect, url):
    """Loop url"""
    print "loop_url(%s)" % url
    generic_looper(IpVideoStream(url).start(), effect)

if __name__ == "__main__":
    (parse_command_line(None))()
    cv2.destroyAllWindows()

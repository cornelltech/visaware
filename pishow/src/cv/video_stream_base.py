"""video_stream_base.py"""

import abc
import unittest
import cv2
from fps import FPS
from threading import Thread
from pacer import Pacer
import time


# stream out FPS
DEFAULT_DESIRED_FPS = 10.0
WINDOW_NAME = "Stream"

class VideoStreamBase:
    """VideoStreamBase"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, desiredFPS=DEFAULT_DESIRED_FPS):
        """Constructor"""
        self.desiredFPS = desiredFPS
        self.fpsCounter = FPS()
        self.pacer = Pacer(desiredFPS)
        self.stopped = True
        self.stream = None
        self.frame = None
        cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)

    def start(self):
        """Start thread to read frames from the file video stream"""
        if self.stream is None:
            raise Exception("Cannot start thread - stream is None")
        if not self.stopped:
            raise Exception("Cannot start thread - a thread is already running")
        self.stopped = False
        thread = Thread(target=self.main_thread, args=())
        thread.daemon = True
        thread.start()
        return self

    @abc.abstractmethod
    def loop_body(self):
        """
        Abstract method that must be implemented for various streams
        that inherit from this base class.

        This method reads new frames every time it is called and sets
        self.frame to a new frame it just read.

        This method also detects the end of stream (e.g. EOF when streaming
        from a file and stops the thread upon such detection.

        This method works in conjunction with the constructor - its
        initialization happens there.
        """
        raise Exception("Not implemented")

    def main_thread(self):
        """Thread body: Keep looping infinitely"""
        self.fpsCounter.start()
        if self.desiredFPS:
            self.pacer.start()

        while True:
            if self.stopped:
                return

            self.loop_body()

            self.fpsCounter.update()
            if self.desiredFPS:
                self.pacer.update()

    def read(self):
        """Return the current frame in the stream"""
        return self.frame

    def stop(self):
        """Stop the thread and FPS counter"""
        self.stopped = True
        self.fpsCounter.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fpsCounter.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fpsCounter.fps()))

    @staticmethod
    def generic_looper(videoStream, effect=None):
        """
        Generic stream receiver loop.  This is the function that runs a
        loop with some OpenCV effect (an effect class that has the
        method apply() as one of its members, which is a method that
        takes in an image frame, does something to it and returns a
        resulting image frame. This function is here so that we don't
        need to write the loop code every time we have to loop over a
        stream.
        """
        pacer = Pacer(DEFAULT_DESIRED_FPS).start()
        while True:
            if videoStream.stopped or cv2.waitKey(30) & 0xFF == ord("q"):
                break

            frame = videoStream.read()
            if frame is not None:
                if effect is not None:
                    frame = effect.apply(frame)
                cv2.imshow(WINDOW_NAME, frame)
                pacer.update()

        # clean up at the end
        videoStream.stop()
        cv2.destroyAllWindows()

"""video_stream_base.py"""

import abc
import unittest
import cv2
from fps import FPS
from threading import Thread
from pacer import Pacer
import time

DEFAULT_FPS = 30.0

class VideoStreamBase:
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, desiredFPS=DEFAULT_FPS):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.desiredFPS = desiredFPS
        self.fpsCounter = FPS()
        self.pacer = Pacer(desiredFPS)
        self.stopped = True
        self.stream = None
        self.frame = None

    def start(self):
        # start a thread to read frames from the file video stream
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
        raise Exception("Not implemented")

    def main_thread(self):
        # keep looping infinitely
        self.fpsCounter.start()
        if self.desiredFPS:
            self.pacer.start()
        while True:
            if self.stopped:
                return
            
            self.loop_body()

            if self.desiredFPS:
                self.pacer.update()

            self.fpsCounter.update()

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.fpsCounter.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fpsCounter.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fpsCounter.fps()))

    @staticmethod
    def generic_looper(videoStream, effect=None):
        """same loop code for any stream"""
        pacer = Pacer(DEFAULT_FPS).start()
        while True:
            if videoStream.stopped or cv2.waitKey(1) & 0xFF == ord("q"):
                break

            frame = videoStream.read()
            if frame is not None:
                if effect is not None:
                    frame = effect.apply(frame)    
                cv2.imshow("Frame", frame)

        # clean up at the end
        videoStream.stop()
        cv2.destroyAllWindows()

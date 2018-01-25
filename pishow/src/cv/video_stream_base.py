"""video_stream_base.py"""

import abc
import unittest
import cv2
from fps import FPS
from threading import Thread
from pacer import Pacer


DEFAULT_FPS = 30.0

class VideoStreamBase:
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, fps=DEFAULT_FPS):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.fps = fps
        self.pacer = Pacer(fps)
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
        self.pacer.start()
        return self

    @abc.abstractmethod
    def loop_body(self):
        raise Exception("Not implemented")

    def main_thread(self):
        # keep looping infinitely
        while True:
            if self.stopped:
                return

            self.loop_body()

            if self.fps:
                self.pacer.update()

    def read(self):
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    @staticmethod
    def generic_looper(videoStream, effect=None):
        """same loop code for any stream"""
        fps = FPS().start()
        pacer = Pacer(DEFAULT_FPS).start()

        while True:
            frame = videoStream.read()

            if frame is not None and not videoStream.stopped:
                if effect is not None:
                    frame = effect.apply(frame)    
                cv2.imshow('Frame', frame)
                fps.update()
                
            if videoStream.stopped or cv2.waitKey(1) & 0xFF == ord('q'):
                break

            pacer.update()

        # clean up at the end
        fps.stop()
        videoStream.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        cv2.destroyAllWindows()

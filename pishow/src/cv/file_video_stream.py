#!/usr/bin/env python
"""file_video_stream.py"""

import unittest
from threading import Thread
import sys
import cv2
# from imutils.video import FPS
from fps import FPS
from pacer import Pacer

DEFAULT_QUEUE_SIZE = 128

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue

class FileVideoStream:
    def __init__(self, path, queueSize=DEFAULT_QUEUE_SIZE):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False

        # initialize the queue used to store frames read from
        # the video file
        self.queue = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            # otherwise, ensure the queue has room in it
            if not self.queue.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return

                # add the frame to the queue
                self.queue.put(frame)

    def read(self):
        # return next frame in the queue
        return self.queue.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.queue.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        videoStream = FileVideoStream(TEST_FILE).start()
        fps = FPS().start()
        pacer = Pacer(DESIRED_FPS).start()

        while True:
            frame = videoStream.read()
            if frame is None:
                print 'frame is none!'
                break;
        
            cv2.imshow('Frame', frame)
            fps.update()
            pacer.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        fps.stop()
        videoStream.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    TEST_FILE = "../../../data/vid02.mov"
    DESIRED_FPS = 30

    unittest.main()

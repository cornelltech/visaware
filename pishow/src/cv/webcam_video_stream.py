#!/usr/bin/env python
"""webcam_video_stream.py"""

# import the necessary packages
import unittest
from threading import Thread
import cv2
# from imutils.video import FPS
from fps import FPS


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        videoStream = WebcamVideoStream().start()
        fps = FPS().start()

        while fps.nFrames < N_TEST_FRAMES:
            frame = videoStream.read()
            if frame is None:
                print 'frame is none!'
                break;
        
            cv2.imshow('Frame', frame)
            fps.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        fps.stop()
        videoStream.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    N_TEST_FRAMES = 1000
    unittest.main()
        

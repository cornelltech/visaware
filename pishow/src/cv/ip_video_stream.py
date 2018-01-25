#!/usr/bin/env python
"""ip_video_stream.py"""

import urllib
import unittest
from threading import Thread
import cv2
from fps import FPS
import numpy


# constant for buffer we hold image data in while streaming from url
BUFFER_LENGTH = 1024
JPEG_START_MARKER = '\xff\xd8'
JPEG_END_MARKER = '\xff\xd9'

class IpVideoStream:
    """Like WebcamVideoStream of imutils.video but for IP cams"""
    def __init__(self, url):
        self.stream = urllib.urlopen(url)
        self.buffer = self.stream.read(BUFFER_LENGTH)
        self.buf2frame()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.frame = None

    def buf2frame(self):
        """Find a jpeg image in raw stream buffer, update accordingly"""
        iStart = self.buffer.find(JPEG_START_MARKER)
        iEnd = self.buffer.find(JPEG_END_MARKER)
        if iStart != -1 and iEnd != -1:
            jpg = self.buffer[iStart:iEnd+2]
            # grab only the leftovers, for next iteration:
            self.buffer = self.buffer[iEnd+2:]
            self.frame = cv2.imdecode(
                numpy.fromstring(jpg, dtype=numpy.uint8), 1)

    def start(self):
        # start the thread to read frames from the video stream
        thread = Thread(target=self.main_thread, args=())
        thread.daemon = True
        thread.start()
        return self

    def main_thread(self):
        # if the thread indicator variable is set, stop the thread
        if self.stopped:
            return

        # keep looping infinitely until the thread is stopped
        while True:
            self.buffer += self.stream.read(BUFFER_LENGTH)
            self.buf2frame()

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
        videoStream = IpVideoStream(TEST_URL).start()
        fps = FPS().start()

        while fps.nFrames < N_TEST_FRAMES:
            frame = videoStream.read()
            if frame is not None:
                cv2.imshow('Frame', frame)
                cv2.waitKey(1) & 0xFF
                fps.update()

        fps.stop()
        videoStream.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    # TEST_URL = 'http://128.84.84.129:8080/?action=stream'
    TEST_URL = 'http://128.84.84.149:8080/?action=stream'
    N_TEST_FRAMES = 1000

    unittest.main()

#!/usr/bin/env python3
"""ip_video_stream.py"""

import unittest
import urllib
import cv2
import numpy
import video_stream_base as base


# constant for buffer we hold image data in while streaming from url
BUFFER_LENGTH = 1024 * 100
JPEG_START_MARKER = '\xff\xd8'
JPEG_END_MARKER = '\xff\xd9'

class IpVideoStream(base.VideoStreamBase):
    """Like WebcamVideoStream of imutils.video but for IP cams"""
    def __init__(self, url, fps=base.DEFAULT_DESIRED_FPS):
        """constructor"""
        super(IpVideoStream, self).__init__(fps)
        self.stream = urllib.urlopen(url)
        self.buffer = ''
        self.iStart = -1
        self.iEnd = -1

    def loop_body(self):
        """Find a jpeg image in raw stream buffer, update accordingly"""
        self.buffer += self.stream.read(BUFFER_LENGTH)

        # iStart = self.buffer.find(JPEG_START_MARKER)
        # iEnd = self.buffer.find(JPEG_END_MARKER)
        # if iStart != -1 and iEnd != -1:
        #     jpg = self.buffer[iStart:iEnd+2]
        #     # grab only the leftovers, for next iteration:
        #     self.buffer = self.buffer[iEnd+2:]
        #     self.frame = cv2.imdecode(
        #         numpy.fromstring(jpg, dtype=numpy.uint8), 1)

        # note this block much slower than version (block) above
        # still, the above version is not as fast as ext_exp01.py
        if self.iStart == -1:
            # we have not found the start marker yet, find it
            self.iStart = self.buffer.find(JPEG_START_MARKER)
        else:
            # found the start marker already, only look for end marker
            self.iEnd = self.buffer.find(JPEG_END_MARKER)
            if self.iEnd != -1:
                # just found end marker, have both start & end now, decode
                jpg = self.buffer[self.iStart:self.iEnd+2]
                # grab only the leftovers, for next iteration:
                self.buffer = self.buffer[self.iEnd+2:]
                self.frame = cv2.imdecode(
                    numpy.fromstring(jpg, dtype=numpy.uint8), 1)
                self.iStart = -1
                self.iEnd = -1

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we do this?"""
        base.VideoStreamBase.generic_looper(IpVideoStream(TEST_URL).start())


if __name__ == "__main__":
    TEST_URL = 'http://128.84.84.129:8080/?action=stream'
    # TEST_URL = 'http://128.84.84.149:8080/?action=stream'
    unittest.main()

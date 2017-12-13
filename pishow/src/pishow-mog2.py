#!/usr/bin/env python

import cv2
import urllib
import numpy

URL = 'http://128.84.84.129:8080/?action=stream'
BUFFER_LENGTH = 1024

stream = urllib.urlopen(URL)
fgbg = cv2.createBackgroundSubtractorMOG2()
bytes = ''
while(True):
    bytes += stream.read(BUFFER_LENGTH)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if  a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        # frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8),
        #                      cv2.CV_LOAD_IMAGE_COLOR)
        frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)

        # cv2.imshow('frame', frame)

        fgmask = fgbg.apply(frame)
        cv2.imshow('frame', fgmask)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            exit(0)

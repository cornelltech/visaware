#!/usr/bin/env python

import cv2
import urllib
import numpy

URL = 'http://128.84.84.129:8080/?action=stream'
BUFFER_LENGTH = 1024

stream = urllib.urlopen(URL)
bytes = ''

while(True):

    bytes += stream.read(BUFFER_LENGTH)

    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')

    if  a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        # img = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8),
        #                    cv2.CV_LOAD_IMAGE_COLOR)
        img = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)

        cv2.imshow('img', img)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()

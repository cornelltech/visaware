#!/usr/bin/env python

import cv2
import urllib
import numpy
import time

URL = 'http://128.84.84.129:8080/?action=stream'
BUFFER_LENGTH = 1024
FONT_LOCATION = (550, 20)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 255
FONT_LINE_TYPE = 1


def main():
    stream = urllib.urlopen(URL)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    bytes = ''
    while(True):
        start_time = time.time()
        bytes += stream.read(BUFFER_LENGTH)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if  a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)

            mog2 = fgbg.apply(frame)

            end_time = time.time()
            fps = 1/(end_time-start_time)

            cv2.putText(mog2, '%2.2f fps' % fps, FONT_LOCATION,
                        FONT, FONT_SCALE, FONT_COLOR, FONT_LINE_TYPE)

            cv2.imshow('MOG2', mog2)

            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                exit(0)

    
if __name__ == '__main__':
    main()
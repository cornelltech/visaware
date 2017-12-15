#!/usr/bin/env python

import cv2
import urllib
import numpy
import time

URL = 'http://128.84.84.129:8080/?action=stream'
BUFFER_LENGTH = 1024
FONT_LOCATION = (550, 460)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 128
FONT_LINE_TYPE = 2

# callback is a function that takes one argument: a color image,
# decoded from the stream without any processing. It processes that image
# and returns a processed image.
def main_loop(callback):
    stream = urllib.urlopen(URL)
    buffer = ''
    start_time = time.time()
    while(True):
        buffer += stream.read(BUFFER_LENGTH)
        image_start = buffer.find('\xff\xd8')
        image_end = buffer.find('\xff\xd9')
        if  image_start != -1 and image_end != -1:
            jpg = buffer[image_start:image_end+2]
            buffer = buffer[image_end+2:]
            frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)
            processed_frame = callback(frame)
            end_time = time.time()
            fps = 1/(end_time-start_time)
            start_time = end_time
            cv2.putText(processed_frame, '%2.2f fps' % fps, FONT_LOCATION,
                        FONT, FONT_SCALE, FONT_COLOR, FONT_LINE_TYPE)
            cv2.imshow('frame', processed_frame)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                exit(0)

def callback(frame):
    return frame

    
if __name__ == '__main__':
    main_loop(callback)

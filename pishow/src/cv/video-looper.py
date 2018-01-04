#!/usr/bin/env python

import cv2
import urllib
import numpy
import time

BUFFER_LENGTH = 1024
FONT_LOCATION = (550, 460)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 128
FONT_LINE_TYPE = 2

# callback is a function that takes one argument: a color image,
# decoded from the stream without any processing. It processes that image
# and returns a processed image.
def main_loop(url=None, filename=None, callback=None):
    if url and filename:
        raise Exception('Supply one of "url" and "filename", not both.')
    if url:
        # capturing from an ip camera at some url
        stream = urllib.urlopen(url)
        buffer = ''
    elif filename:
        # capturing from file
        cap = cv2.VideoCapture(filename)
    else:
        # capturing from camera on the device where this script runs
        cap = cv2.VideoCapture(0)

    done = False
    start_time = time.time()
    while(True):
        if url: 
            buffer += stream.read(BUFFER_LENGTH)
            image_start = buffer.find('\xff\xd8')
            image_end = buffer.find('\xff\xd9')
            ret = False
            if image_start != -1 and image_end != -1:
                jpg = buffer[image_start:image_end+2]
                buffer = buffer[image_end+2:]
                frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8),1)
                ret = True
        else:
            ret, frame = cap.read()

        if ret:
            # a frame has been grabbed in 'frame'
            if callback:
                processed_frame = callback(frame)
            else:
                processed_frame = frame

            # show FPS
            end_time = time.time()
            fps = 1/(end_time-start_time)
            start_time = end_time
            cv2.putText(processed_frame, '%2.2f fps' % fps, FONT_LOCATION,
                        FONT, FONT_SCALE, FONT_COLOR, FONT_LINE_TYPE)

            # show image
            cv2.imshow('frame', processed_frame)
        elif not done:
            # capture has finished, report that (only once) here
            done = True
            print 'Captured clip has ended!'

        # listen to quit keystroke
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if cap:
                cap.release()
            cv2.destroyAllWindows()
            exit(0)


if __name__ == '__main__':
    main_loop('http://128.84.84.129:8080/?action=stream')
    # main_loop(None, '../../../data/vid02.mov')

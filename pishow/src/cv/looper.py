#!/usr/bin/env python
"""looper.py"""

# Main loop and command line argument parsing and image display with FPS

import sys
import urllib
import time
import numpy
import cv2


# constants for fps display overlayed on the (640px x 480px) image
FONT_LOCATION = (550, 460)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 64
FONT_LINE_TYPE = 2

# constant for buffer we hold image data in while streaming from url
BUFFER_LENGTH = 1024

def parse_command_line(effect):
    """Process command line arguments"""
    progname = sys.argv[0]
    usage_message = 'Usage: %s [<url>|<file-path>]\n' % progname
    n_args = len(sys.argv)-1
    if n_args == 0:
        return lambda: loop_camera_or_file(effect, 0)
    elif n_args == 1:
        arg = sys.argv[1]
        if arg == '-h' or arg == '--help':
            print usage_message
            sys.exit(0)
        elif arg[0:4] == 'http':
            return lambda: loop_url(effect, arg)
        else:
            return lambda: loop_camera_or_file(effect, arg)
    else:
        print usage_message
        raise Exception('Only one argument allowed, you gave %d' % n_args)

def loop_camera_or_file(effect, loop_what):
    """Loop camera or file"""
    if loop_what == 0:
        print 'loop_camera()'
    else:
        print 'loop_file(%s)' % loop_what
    cap = cv2.VideoCapture(loop_what)
    done = False
    start_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # process frame
            processed_frame = frame
            if effect:
                processed_frame = effect.apply(frame)
            end_time = time.time()
            show_image_w_fps(processed_frame, 1/(end_time-start_time))
            start_time = end_time
        elif not done:
            done = True
            print 'Clip ended!'

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # cleanup after breaking out of the while loop
    cap.release()

def loop_url(effect, url):
    """Loop url"""
    print 'loop_url(\'%s\')' % url
    stream = urllib.urlopen(url)
    buf = ''
    start_time = time.time()
    while True:
        buf += stream.read(BUFFER_LENGTH)
        image_start = buf.find('\xff\xd8')
        image_end = buf.find('\xff\xd9')
        if image_start != -1 and image_end != -1:
            # got a complete frame, decode it
            jpg = buf[image_start:image_end+2]
            buf = buf[image_end+2:]
            frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)
            # process frame
            processed_frame = frame
            if effect:
                processed_frame = effect.apply(frame)
            end_time = time.time()
            show_image_w_fps(processed_frame, 1.0/(end_time-start_time))
            start_time = end_time

        # listen to quit keystroke
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def show_image_w_fps(frame, fps):
    """refresh the display with contents of frame and show fps"""
    cv2.putText(frame, '%2.2f fps' % fps, FONT_LOCATION,
                FONT, FONT_SCALE, FONT_COLOR, FONT_LINE_TYPE)
    cv2.imshow('frame', frame)


if __name__ == '__main__':
    (parse_command_line(None))()
    cv2.destroyAllWindows()

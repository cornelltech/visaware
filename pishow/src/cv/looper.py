#!/usr/bin/env python

import sys
import cv2
import urllib
import numpy
import time

# constants for fps display overlayed on the (640px x 480px) image
FONT_LOCATION = (550, 460)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = 64
FONT_LINE_TYPE = 2

def parse_command_line(callback):
    """Process command line arguments"""
    progname = sys.argv[0]
    usage_message = 'Usage: %s [url=<url>|file=<path>]\n' % progname
    n_args = len(sys.argv)-1
    if n_args == 0:
        return lambda: loop_camera_or_file(callback, 0)
    elif n_args == 1:
        arg = sys.argv[1]
        if arg == '-h' or arg == '--help':
            print usage
            sys.exit(0)
        args = arg.split('=')
        if len(args) != 2:
            raise Exception('Malformed argument')
        arg_name = args[0].strip()
        arg_value = args[1].strip()
        if arg_name == '' or arg_value == '':
            raise Exception('Malformed argument')
        if arg_name == 'url':
            return lambda: loop_url(callback, arg_value)
        elif arg_name == 'file':
            return lambda: loop_camera_or_file(callback, arg_value)
    else:
        print usage_message
        raise Exception('Only one argument allowed, you gave %d' % n_args)

def loop_camera_or_file(callback, loop_what):
    """Loop camera or file"""
    if loop_what == 0:
        print 'loop_camera()'
    else:
        print 'loop_file(%s)' % loop_what
    cap = cv2.VideoCapture(loop_what)
    done = False
    start_time = time.time()
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # process frame
            processed_frame = frame
            if callback:
                processed_frame = callback(frame)
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

def loop_url(callback, url):
    """Loop url"""
    print 'loop_url(\'%s\')' % url
    stream = urllib.urlopen(url)
    buffer = ''
    start_time = time.time()
    while(True):
        buffer += stream.read(BUFFER_LENGTH)
        image_start = buffer.find('\xff\xd8')
        image_end = buffer.find('\xff\xd9')
        if image_start != -1 and image_end != -1:
            # got a complete frame, decode it
            jpg = buffer[image_start:image_end+2]
            buffer = buffer[image_end+2:]
            frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 1)
            # process frame
            processed_frame = frame
            if callback:
                processed_frame = callback(frame)
            end_time = time.time()
            show_image_w_fps(processed_frame, 1/(end_time-start_time))
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
    (looper.parse_command_line(None))()
    cv2.destroyAllWindows()

#!/usr/bin/env python

import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from avg_frames_on_button_click130 import AvgFramesOnButton


WINDOW_NAME = 'cam'

class Cam():

    def __init__(self, url):

        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        self.avg = AvgFramesOnButton()
        cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                                    cv2.WINDOW_FULLSCREEN)
        print "camera initialised"


    def start(self):
        self.thread.start()
        print "camera stream started"

    def run(self):
        bytes=''
        while not self.thread_cancelled:
            try:
                bytes+=self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                                         cv2.IMREAD_COLOR)

                    img = self.avg.apply(img)

                    cv2.imshow(WINDOW_NAME,img)
                    if cv2.waitKey(1) ==27:
                        exit(0)
            except ThreadError:
                self.thread_cancelled = True


    def is_running(self):
        return self.thread.isAlive()


    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        return True



if __name__ == "__main__":
    url = 'http://128.84.84.149:8080/?action=stream'
    cam = Cam(url)
    cam.start()

#!/usr/bin/env python3

import numpy as np
import cv2
import requests
from threading import Thread, Event, ThreadError
from fps import FPS


STREAM_URL = 'http://128.84.84.129:8080/?action=stream'
WINDOW_NAME = 'cam'

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def is_running(self):
        return not self._stop_event.is_set()

class Cam():
    def __init__(self):
        self.stream = requests.get(STREAM_URL, stream=True)
        self.thread = StoppableThread(target=self.run)
        self.fps = FPS()
        print("camera initialised")

    def start(self):
        self.thread.start()
        print("camera stream started")

    def run(self):
        self.fps.start()
        bytes = b''
        while self.thread.is_running():
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                       cv2.IMREAD_COLOR)
                    cv2.imshow(WINDOW_NAME, img)
                    self.fps.update()
                    if cv2.waitKey(1) == 27:
                        print('Got Escape key, stopping')
                        self.fps.stop()
                        print("Elasped time: {:.2f}".format(self.fps.elapsed()))
                        print("n_frames: {:.2f}".format(self.fps.n_frames))
                        print("FPS: {:.2f}".format(self.fps.fps()))
                        self.thread.stop()


            except ThreadError:
                self.thread.stop()


if __name__ == "__main__":
    Cam().start()

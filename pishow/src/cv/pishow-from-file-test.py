#!/usr/bin/env python

# show stream in half size

import cv2
import pishow

CAP = cv2.VideoCapture('../../../data/vid02.mov')

while (CAP.isOpened()):
    ret, frame = CAP.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

CAP.release()
cv2.destroyAllWindows()

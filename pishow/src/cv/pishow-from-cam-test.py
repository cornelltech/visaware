#!/usr/bin/env python

# show stream in half size

import cv2
import pishow

CAP = cv2.VideoCapture(0)

done = False
while (CAP.isOpened()):
    ret, frame = CAP.read()

    if ret:
        cv2.imshow('frame', frame)
    elif not done:
        done = True
        print 'Clip ended!'

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

CAP.release()
cv2.destroyAllWindows()

# visaware/pishow/src/cv/

This directory contains the source code of all computer vision related
stuff done on the pishow board.

## Installation
1) Pull code from github
2) Cd to cv directory
3) Type `workon cv2` before running any code
4) `./<run-code>.py`

## Contents
File or directory name | Purpose
---------------------- | -------
looper.py | Generic OpenCV loop with no processing - just grabs frames from the stream as quickly as possible and displays them as-is. Every other python file in this directory is an effect that does some processing and is based on looper for (a) parsing command line args to decide if to loop video from the built-in camera or from a file or from a URL; (b) display the processed version of each image frame grabbed, with the frames per second (FPS) overlayed on the processed image
mog2.py | Uses the background subtraction method MOG2 built into OpenCV to show frame differences
log_dog.py | A transform that removes illumination, showing reflectance alone (for the most part)
log_dog_mog2.py | Background differencing on the above log-dog transform, should be more robust to bad lighting variations
absdiff | Subtracts current frame - previous frame and takes absolute value of that difference
log_dog_absdiff.py | Background differencing via absdiff on the above log-dog transform, should be more robust to bad lighting variations

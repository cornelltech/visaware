# visaware/pishow/src/cv/

This directory contains the source code of all computer vision related
stuff done on the pishow board.

## Contents
File or directory name | Purpose
---------------------- | -------
pishow.py              | Generic OpenCV loop with no processing - just grabs frames from the stream as quickly as possible and displays them as-is.
pishow-mog2.py         | Uses the background subtraction method MOG2 built into OpenCV to show frame differences

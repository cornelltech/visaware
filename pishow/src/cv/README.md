# visaware/pishow/src/cv/

This directory contains the source code of all computer vision related
stuff done on the pishow board.

## Contents
File or directory name | Purpose
---------------------- | -------
looper.py | Generic OpenCV loop with no processing - just grabs frames from the stream as quickly as possible and displays them as-is.
looper_mog2.py | Uses the background subtraction method MOG2 built into OpenCV to show frame differences
looper_mog2?.py | Variations on above
looper_log_dog.py | A transform that removes illumination, showing reflectance alone (for the most part)
looper_log_dog_mog2.py | Background differencing onthe above log-dog transform, should be more robust to bad lighting variations

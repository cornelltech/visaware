#!/bin/bash

# this is the script that runs mjpeg_streamer as user pi every time
# this device boots. it is called from /etc/rc.local during the boot
# process.

# this script contains all the command-line arguments that we want to supply
# mjpeg_streamer for our operations.  to change the command-line arguments of
# mjpeg_streamer server, change them here and only here.

# NOTE: mjpeg_streamer has been installed in user 'pi' home directory.
# The final install step 'sudo make install' put files under /usr/local/

# mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -br 90 -co 100 -ifx watercolour" -o "output_http.so -w ./www"

# add instead -i "input_uvc.so -r 1080x720 -n" or any other resolution for USB webcam 
#also adding effects: for example  -ifx sketch
# mjpg_streamer \
#     -i "input_raspicam.so -awb -x 640 -y 480 -fps 30" \
#     -o "output_http.so -w ./www"

mjpg_streamer \
    -i "input_raspicam.so -awb -x 640 -y 480 -fps 30" \
    -o "output_http.so -w ./www"

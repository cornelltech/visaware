#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

export WORKON_HOME=/home/pi/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

workon cv2

HOSTNAME=`hostname -s`

# determine which pishow we're on and stream from the right pisee accordingly
if [ "$HOSTNAME" == "pishow-150" ]; then
    # STREAM_IP="128.84.84.129"
    STREAM_IP="128.84.84.149"
else
    # we are running this from pishow-130, not -150
    # STREAM_IP="128.84.84.149"
    STREAM_IP="128.84.84.129"
fi

if [ "$HOSTNAME" == "pishow-150" ]; then
    BOOT_EXEC="/home/pi/workspace/visaware/pishow/src/cv/ext_exp01m-150.py"
else
    BOOT_EXEC="/home/pi/workspace/visaware/pishow/src/cv/ext_exp01m-130.py"
fi

BOOT_EXEC="/home/pi/workspace/visaware/pishow/src/cv/ext_exp01m.py"
LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"

echo "boot_script.sh: STREAM_IP=$STREAM_IP"


DISPLAY=:0 $BOOT_EXEC http://${STREAM_IP}:8080/?action=stream >> $LOG_FILE 2>&1

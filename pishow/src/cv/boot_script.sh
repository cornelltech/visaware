#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

export WORKON_HOME=/home/pi/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

workon cv2

setterm -blank 0 -powerdown 0

BOOT_EXEC="/home/pi/workspace/visaware/pishow/src/cv/ext_exp01m.py"
LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"

echo "boot_script.sh: STREAM_IP=$STREAM_IP"

DISPLAY=:0 $BOOT_EXEC >> $LOG_FILE 2>&1

#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

export WORKON_HOME=/home/pi/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

workon cv2

HOSTNAME=`hostname -s`

# determine which pishow we're on and stream from the right pisee accordingly
if [ "$HOSTNAME" == "pishow-150" ]; then
    # STREAM_IP="128.84.84.129
    STREAM_IP="128.84.84.149"
else
    # STREAM_IP="128.84.84.149"
    STREAM_IP="128.84.84.129"
fi

BOOT_EXEC="$HOME/workspace/visaware/pishow/src/cv/avg_frames_on_button_click.py"
# LOG_FILE="~/logs/boot_script_`date +%F`.log"
LOG_FILE="$HOME/logs/boot_script.log"

DISPLAY=:0 $BOOT_EXEC http://${STREAM_IP}:8080/?action=stream >> $LOG_FILE 2>&1

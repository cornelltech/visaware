#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

# This script is started on a Raspberry Pi board that has been set up for
# 1) Automatic login of user pi into a graphical desktop (to set this auto-
#    login up, use the command `sudo raspi-config`)
# 2) Add the following line to `/home/pi/.config/lxsession/LXDE/autostart`:
# @lxterminal --command="/home/pi/workspace/visaware/pishow/src/boot_script.sh"

# The IP of the other pishow board that this board communicates with

setterm -powerdown 0

MY_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo $MY_DIR

CMD="$MY_DIR/avg_frames_on_button_click.py"

ARG="http://128.84.84.129:8080/?action=stream"

LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"

echo "boot_script.sh: starting..."
DISPLAY=:0 "$CMD" "$ARG" >> "$LOG_FILE" 2>&1

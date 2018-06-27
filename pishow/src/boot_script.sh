#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

# This script is started on a Raspberry Pi board that has been set up for
# 1) Automatic login of user pi into a graphical desktop (to set this auto-
#    login up, use the command `sudo raspi-config`)
# 2) Add the following line to `/home/pi/.config/lxsession/LXDE-pi/autostart`:
# @lxterminal --command="/home/pi/workspace/visaware/pishow/src/boot_script.sh"

################################################################################
# The IP numbers (you may need to change these three ip-numbers)

# NOTE: IP numbers we use for testing:
# pisee-129 (near Benny's desk):  128.84.84.129
# pishow-130 (near Benny's desk): 128.84.84.130
# pisee-149 (CX lab):             128.84.84.149
# pishow-150 (CX lab):            128.84.84.150

# Use these numbers on pishow in CX lab:

# MY_IP is the IP number of the pishow board on which this code is running:
# MY_IP="128.84.84.150"
# OTHER_IP is the IP number of the other pishow board this one communicates with
# OTHER_IP="128.84.84.130"
# WEBCAM_URL is the full URL of the pisee board or any webcam used near OTHER_IP
# WEBCAM_URL="http://128.84.84.129:8080/?action=stream"

# Use these numbers on pishow near Benny's desk:

# MY_IP is the IP number of the pishow board on which this code is running:
MY_IP="128.84.84.130"
# OTHER_IP is the IP number of the other pishow board this one communicates with
OTHER_IP="128.84.84.150"
# WEBCAM_URL is the full URL of the pisee board or any webcam used near OTHER_IP
WEBCAM_URL="http://128.84.84.149:8080/?action=stream"
################################################################################

# Do not change anything below

MY_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"
CMD="$MY_DIR/avg_frames_on_button_click.py"

echo "----------------------------------------------------------" >> "$LOG_FILE"
echo "`date` - boot_script.sh: starting .." >> "$LOG_FILE"
echo "----------------------------------------------------------" >> "$LOG_FILE"

setterm -powerdown 0
DISPLAY=:0 "$CMD" "$MY_IP" "$OTHER_IP" "$WEBCAM_URL" >> "$LOG_FILE" 2>&1


#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.
#
# NOTES: do not change the code in this script. You control it by changing
# values in other files, in the same directory (folder) as this script:
#
# To change screen resolution (it depends on your screen or screen)
# change it in the file SCREEN_RESOLUTION
#
# To change the IP address of the other Raspberry Pi board to which you are
# sending commands - the one that is connected to the projector or screen on
# the other end, change the IP address in the file OTHER_PISHOW_IP_ADDRESS
#
# To change the URL of the webcam you are using on the other end, change
# the full URL of the webcam's stream in the file WEBCAM_STREAM_URL 
#
# This script is started on a Raspberry Pi board that has been set up for
# 1) Automatic login of user pi into a graphical desktop (to set this auto-
#    login up, use the command `sudo raspi-config`)
# 2) Add the following line to `/home/pi/.config/lxsession/LXDE-pi/autostart`:
# @lxterminal --command="/home/pi/workspace/visaware/pishow/src/boot_script.sh"

MY_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# full-screen width & height of screen
WIDTH="`cat $MY_DIR/SCREEN_RESOLUTION | sed 's/x/ /' | awk '{print $1}'`"
HEIGHT="`cat $MY_DIR/SCREEN_RESOLUTION | sed 's/x/ /' | awk '{print $2}'`"
MY_IP="`ifconfig | grep -A 1 eth0 | grep inet | awk '{print $2}'`"
OTHER_IP="`cat $MY_DIR/OTHER_PISHOW_IP_ADDRESS`"
WEBCAM_URL="`cat $MY_DIR/WEBCAM_STREAM_URL`"

# make sure the logs directory exists
mkdir -p "/home/pi/logs"

LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"
CMD="$MY_DIR/avg_frames_on_button_click.py"

echo "----------------------------------------------------------" >> "$LOG_FILE"
echo "`date` - boot_script.sh: starting .." >> "$LOG_FILE"
echo "Fullscreen size: ${WIDTH}x$HEIGHT" >> "$LOG_FILE"
echo "My (pishow) IP: $MY_IP" >> "$LOG_FILE"
echo "Other (pishow) IP: $OTHER_IP" >> "$LOG_FILE"
echo "Webcam URL: $WEBCAM_URL" >> "$LOG_FILE"
echo "----------------------------------------------------------" >> "$LOG_FILE"

setterm -powerdown 0

# the following line logs board temperature every 10 seconds:
# ( while true; do vcgencmd measure_temp; sleep 10; done >> "$LOG_FILE" ) &

DISPLAY=:0 "$CMD" "$MY_IP" "$OTHER_IP" "$WEBCAM_URL" "$WIDTH" "$HEIGHT" \
       >> "$LOG_FILE" 2>&1

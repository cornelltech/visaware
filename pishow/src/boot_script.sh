
#!/bin/bash

# This is the script that user pi runs on pishow boot. This starts everything.

# This script is started on a Raspberry Pi board that has been set up for
# 1) Automatic login of user pi into a graphical desktop (to set this auto-
#    login up, use the command `sudo raspi-config`)
# 2) Add the following line to `/home/pi/.config/lxsession/LXDE-pi/autostart`:
# @lxterminal --command="/home/pi/workspace/visaware/pishow/src/boot_script.sh"

setterm -powerdown 0

MY_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
CMD="$MY_DIR/avg_frames_on_button_click.py"
LOG_FILE="/home/pi/logs/boot_script`date +%F`.log"

echo "`date +%F` -- boot_script.sh: starting..." >> "$LOG_FILE"
DISPLAY=:0 "$CMD" >> "$LOG_FILE" 2>&1

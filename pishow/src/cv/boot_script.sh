#!/bin/bash

export WORKON_HOME=/home/pi/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

workon cv2

DISPLAY=:0 /home/pi/workspace/visaware/pishow/src/cv/avg_frames_on_button_click.py http://128.84.84.129:8080/?action=stream

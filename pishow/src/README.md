## visaware/pishow/src/

This directory contains all source code running on the pishow board
for the visaware project.

### Installation - get a pishow board up and running
1) Get an SD-card with Raspbian OS installed on it to boot with
   *Current version is Raspbian 9 (stretch)*
2) [Optional] Set the hostname using `raspi-config`
3) Set the time zone using `raspi-config`
4) Enable GPIO using `raspi-config`
5) Clone the following two repositories into the same parent folder:
   * [https://github.com/cornelltech/opencv-video-loops](https://github.com/cornelltech/opencv-video-loops)  
   * [https://github.com/cornelltech/visaware](https://github.com/cornelltech/visaware)  
6) Copy the file `autostart` (in this directory) as follows
   `cp autostart /home/pi/.config/lxsession/LXDE-pi/
7) Create the following three files in this direcotry:

Filename                | What to put in it (example)
----------------------- | ---------------------------
OTHER_PISHOW_IP_ADDRESS | 128.84.84.130
SCREEN_RESOLUTION | 1024x768
WEBCAM_STREAM_URL | http://128.84.84.129:8080/?action=stream


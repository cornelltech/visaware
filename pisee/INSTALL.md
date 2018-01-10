# pysee installation

1) Grab a blank micro-sd card and install the Raspbian OS on it in the most
generic way possible. Download the image [here](https://www.raspberrypi.org/downloads/raspbian/) and follow instructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
2) This step is optional but recommended - format the SD card when you first get it out of the packaging - that's because the formatting process checks and marks bad blocks and those SD cards do have them sometimes.
3) On OS X, you can use `etcher` to write the OS image to the micro-sd card.
NOTE: despite what the installation instructions tell you (to unzip the zip file before using etcher), do not unzip the zip file. Instead, when etcher asks what you want to etch (where is the image file) just load up the zip file you've downloaded and it will be burned onto the sd-card.
4) Upgrade and update packages. Insert micro-sd card into board and boot it,
start a shell and type 
    ```
    sudo apt update
    sudo apt upgrade
    ```
5) Change the keyboard layout from UK (Raspberry Pi default) to a US keyboard. To do this, first type in a shell on the Pi:
   ```
   sudo dpkg-reconfigure keyboard-configuration
   ```
   Choose "Generic 104 key" for most US keyboards.  Choose US keyboard next - pick the default one (top of the list).
6) Change the keyboard to a US keyboard (because by default the board comes
with a UK keyboard). Type
    ```
    sudo dpkg-reconfigure keyboard-configuration
    ```
7) Fix the clock to have the correct time zone via
   ```
   sudo dpkg-reconfigure tzdata
   ```
8) Configure the board with
    ```
    sudo raspi-config
    ```
   Here we want to
   * Enable the camera
   * Set the board's hostname to `pysee`
   * Set password for user `pi`
9) Create two directories under `/home/pi`: 

   File or directory name | Purpose
   ---------------------- | -------
   bin/                   | Scripts that user `pi` may want to run
   workspace/             | Software that user `pi` may want to build

10) Build `mjpg-streamer` in  a subdirectory of 'workspace/', using this 
experimental (raspicam) version: [https://github.com/jacksonliam/mjpg-streamer/](https://github.com/jacksonliam/mjpg-streamer/). Build this all the way up to and including the command
    ```
    sudo make install
    ```
   which will place installed files under `/usr/local/`

11) In `bin/` we currently have the script that is responsible for running the
`mjpg-streamer` executable you've built in the previous step. This script is
where we set the command-line arguments we run `mjpeg-streamer` with. Currently it runs the following code:
    ```
    mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -br 90 -co 100 -ifx watercolour" -o "output_http.so -w ./www"
    ```
12) Set up the machine for automatically starting mjpeg-streamer upon boot (headless or not).  For this just add the following line to `/etc/rc.local`:
    ```
    /home/pi/bin/run_mjpg_streamer.sh > /dev/null 2>&1
    ```

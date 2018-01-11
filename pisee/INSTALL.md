# pysee installation

1) Download latest version of Raspbian OS image and install it via instructions
   [here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
2) Insert the newly created SD card into the Raspberry Pi and boot it with a
   connected monitor, keyboard and mouse. It should end boot showing user pi's
   desktop.
3) Turn off bluetooth via the desktop's top right bluetooth icon
4) Request static IP addresses from suppport@tech.cornell.edu by giving them
   the MAC address of your device, which you can find by issuing the command 
   `ifconfig` and looking for the 'HW Addr' entry in the section that
   corresponds to device `ethX` (typically `eth0`)
5) While you wait for static IP, to continue setting thigns up,
   connect via Wi-Fi via the top right WiFi icon
6) Start a shell (click on the terminal icon on the top right) and 
   upgrade / update system packages:
   ```
   sudo apt update
   sudo apt upgrade
   ```
7) Change the keyboard layout from UK (Raspberry Pi default) to a US keyboard.
   To do this, first type in a shell on the Pi:
   ```
   sudo dpkg-reconfigure keyboard-configuration
   ```
   Choose "Generic 104 key" for most US keyboards.  Choose US keyboard next -
   pick the default one (top of the list).
8) Fix the clock to have the correct time zone via
   ```
   sudo dpkg-reconfigure tzdata
   ```
9) Configure the board with
   ```
   sudo raspi-config
   ```
   Here we want to
   * Enable the camera
   * Set the board's hostname to `pysee`
   * Set password for user `pi`
10) Create two directories under `/home/pi`: 

    File or directory name | Purpose
    ---------------------- | -------
    bin/                   | Scripts that user `pi` may want to run
    workspace/             | Software that user `pi` may want to build

11) Build `mjpg-streamer` in  a subdirectory of 'workspace/', using this
    experimental (raspicam) version: 
    [https://github.com/jacksonliam/mjpg-streamer/](https://github.com/jacksonliam/mjpg-streamer/). 
    Build this all the way up to and including the command
    ```
    sudo make install
    ```
    which will place installed files under `/usr/local/`

12) In `bin/` we currently have the script that is responsible for running the
    `mjpg-streamer` executable you've built in the previous step. This script is
    where we set the command-line arguments we run `mjpeg-streamer` with. 
    Currently it runs the following code:
    ```
    mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -br 90 -co 100 -ifx watercolour" -o "output_http.so -w ./www"
    ```
13) Set up the machine for automatically starting mjpeg-streamer upon boot 
    (headless or not).  For this just add the following line to `/etc/rc.local`:
    ```
    /home/pi/bin/run_mjpg_streamer.sh > /dev/null 2>&1
    ```

# pysee installation

1) Download latest version of Raspbian OS image and install it via instructions
[here](https://www.raspberrypi.org/documentation/installation/installing-images/README.md). Here's a quick shell transcript of a session that does the above:
   ```
   dtal@thing4: sudo fdisk -l
   ...
   Device         Boot Start      End  Sectors  Size Id Type
   /dev/mmcblk0p1       8192 62521343 62513152 29.8G  b W95 FAT32
   dtal@thing4: unzip -p /home/dtal/Downloads/2017-11-29-raspbian-stretch.zip | sudo dd of=/dev/mmcblk0p1 bs=4M status=progress conv=fsync
   4919263232 bytes (4.9 GB, 4.6 GiB) copied, 628.008 s, 7.8 MB/s 
   0+49259 records in
   0+49259 records out
   ```
2) Insert the newly created SD card into the Raspberry Pi and boot it with a
   connected monitor, keyboard and mouse. It should end boot showing user pi's
   desktop.
3) Start a shell (click on the terminal icon on the top right) and 
   upgrade / update system packages:
   ```
   sudo apt update
   sudo apt upgrade
   ```
4) Change the keyboard layout from UK (Raspberry Pi default) to a US keyboard. To do this, first type in a shell on the Pi:
   ```
   sudo dpkg-reconfigure keyboard-configuration
   ```
   Choose "Generic 104 key" for most US keyboards.  Choose US keyboard next - pick the default one (top of the list).
5) Change the keyboard to a US keyboard (because by default the board comes
with a UK keyboard). Type
    ```
    sudo dpkg-reconfigure keyboard-configuration
    ```
6) Fix the clock to have the correct time zone via
   ```
   sudo dpkg-reconfigure tzdata
   ```
7) Configure the board with
    ```
    sudo raspi-config
    ```
   Here we want to
   * Enable the camera
   * Set the board's hostname to `pysee`
   * Set password for user `pi`
8) Create two directories under `/home/pi`: 

   File or directory name | Purpose
   ---------------------- | -------
   bin/                   | Scripts that user `pi` may want to run
   workspace/             | Software that user `pi` may want to build

9) Build `mjpg-streamer` in  a subdirectory of 'workspace/', using this 
experimental (raspicam) version: [https://github.com/jacksonliam/mjpg-streamer/](https://github.com/jacksonliam/mjpg-streamer/). Build this all the way up to and including the command
    ```
    sudo make install
    ```
   which will place installed files under `/usr/local/`

10) In `bin/` we currently have the script that is responsible for running the
`mjpg-streamer` executable you've built in the previous step. This script is
where we set the command-line arguments we run `mjpeg-streamer` with. Currently it runs the following code:
    ```
    mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -br 90 -co 100 -ifx watercolour" -o "output_http.so -w ./www"
    ```
11) Set up the machine for automatically starting mjpeg-streamer upon boot (headless or not).  For this just add the following line to `/etc/rc.local`:
    ```
    /home/pi/bin/run_mjpg_streamer.sh > /dev/null 2>&1
    ```

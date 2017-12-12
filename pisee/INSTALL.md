# pysee installation

1) Grab a blank micro-sd card and install the Raspbian OS on it in the most
generic way possible. Download the image and follow instructions [here]
(https://www.raspberrypi.org/downloads/raspbian/).
2) On a mac, I used `etcher` to write the OS image to the micro-sd card
3) Upgrade and update packages. Insert micro-sd card into board and boot it,
start a shell and type 
    ```
    sudo apt update
    sudo apt upgrade
    ```
4) Change the keyboard to a US keyboard (because by default the board comes
with a UK keyboard). Type
    ```
    sudo dpkg-reconfigure keyboard-configuration
    ```
5) Configure the board with
    ```
    sudo raspi-config
    ```
   Here we want to
   * Enable the camera
   * Set the board's hostname to `pysee`
   * Set password for user `pi`
6) Create two directories

   File or directory name | Purpose
   ---------------------- | -------
   bin/                   | Scripts that user `pi` may want to run
   workspace/             | Software that user `pi` may want to build

7) Build `mjpg-streamer` in  a subdirectory of 'workspace/', using this 
experimental (raspicam) version: [https://github.com/jacksonliam/mjpg-streamer/](https://github.com/jacksonliam/mjpg-streamer/). Build this all the way up to and including the command
    ```
    sudo make install
    ```
   which will place installed files under `/usr/local/`

8) In `bin/` we currently have the script that is responsible for running the
`mjpg-streamer` executable you've built in the previous step. This script is
where we set the command-line arguments we run `mjpeg-streamer` with. Currently it runs the following code:
    ```
    mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -br 90 -co 100 -ifx watercolour" -o "output_http.so -w ./www"
    ```
9) Set up the machine for automatically starting mjpeg-streamer upon boot (headless or not).  For this just add the following line to `/etc/rc.local`:
    ```
    /home/pi/bin/run_mjpg_streamer.sh > /dev/null 2>&1
    ```

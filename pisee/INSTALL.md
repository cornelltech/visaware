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
10) Clone the git repository `visaware` under institution `cornelltech` on 
    github.
    ```
    mkdir /home/pi/workspace
    cd /home/pi/workspace
    git clone http://github.com/cornelltech/visaware
    ```
11) Create two directories under `/home/pi`: 

    File or directory name | Purpose
    ---------------------- | -------
    `bin/`                 | Scripts that user `pi` may want to run
    `workspace/`           | Software that user `pi` may want to build
12) Grab the visaware repository:
    ```
    cd /home/pi/workspace
    git clone https://github.com/cornelltech/visaware
    ```
12) On `pisee` boards (ones with a camera) you will need `mjpeg_streamer` - 
    here is how you build it: 
    * Build `mjpg-streamer` in  a subdirectory of 
      `workspace/`, using this experimental (raspicam) version: 
      [https://github.com/jacksonliam/mjpg-streamer/](https://github.com/jacksonliam/mjpg-streamer/). 
      Use the instructions at the root of the github repository 
      (a la README.md file there). NOTE: use the `cmake` version of the build
      instructions, i.e, build via `cmake` first. Here's a transcript:
      ```
      sudo ap install cmake libjpeg8-dev
      cd /home/pi/workspace/
      git clone https://github.com/jacksonliam/mjpg-streamer
      cd mjpg-streamer/mjpg-streamer-experimental
      mkdir _build
      cd _build
      export LD_LIBRARY_PATH=.
      cmake ..
      make
      sudo make install
      ```
      which will place installed executable under `/usr/local/mjpg_streamer`
    * Link the wrapper script `run_mjpeg_streamer.sh`, where we set the
      command-line arguments we run `mjpeg-streamer` with, by issuing:
      ```
      ln -s /home/pi/workspace/visaware/pisee/src/run_mjpg_streamer.sh /home/pi/bin/
      ```
13) Set up the machine for automatically starting mjpeg-streamer upon boot 
    (headless or not).  For this just add the following line to `/etc/rc.local`:
    ```
    /home/pi/bin/run_mjpg_streamer.sh > /dev/null 2>&1
    ```

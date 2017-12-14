# pyshow installation

Steps 1-6 are the same as steps 1-5 of [pisee installation instructions](https://github.com/cornelltech/visaware/blob/master/pisee/INSTALL.md)

7) Configure the board with
    ```
    sudo raspi-config
    ```
   Here we want to
   * Set the board's hostname to `pyshow`
   * Set password for user `pi`
8) Create two directories under `/home/pi`: 

   File or directory name | Purpose
   ---------------------- | -------
   bin/                   | Scripts that user `pi` may want to run
   workspace/             | Software that user `pi` may want to build
9) Install and compile OpenCV - follow instructions [as described here](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) to the tee.

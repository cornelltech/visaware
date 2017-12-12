# pyshow installation

1-4) Same as [steps 1-4 of pisee installation]
(https://github.com/cornelltech/visaware/blob/master/pisee/INSTALL.md)
5) Configure the board with
    ```
    sudo raspi-config
    ```
   Here we want to
   * Set the board's hostname to `pyshow`
   * Set password for user `pi`
6) Create two directories under `/home/pi`: 

   File or directory name | Purpose
   ---------------------- | -------
   bin/                   | Scripts that user `pi` may want to run
   workspace/             | Software that user `pi` may want to build

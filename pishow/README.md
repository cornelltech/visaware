# visaware/pishow/

This directory contains all files, code, notes and documentation related to the 
the Raspberry Pi board showing/displaying/projecting the video.

## Throughput (FPS) experiments
Some benchmarking experiments with various setups:

We tried various setups to speed up frames per second.

Show CPU | See CPU | FPS (no processing) | FPS (with processing)
-------- | -------------- | ------------------- | ---------------------
PC laptop | PC laptop built in Camera | 30 | 30
PC laptop | Pisee | 5 | 4.9
Mac Mini | Pisee | 0.57 | 0.56
Pishow | Pisee | 4 | 3.5

### FPS issues solved
Arnaud pointed us to the solution: use multi-threading.

Show CPU | See CPU | FPS (no processing) | FPS (with processing)
-------- | -------------- | ------------------- | ---------------------
PC laptop | PC laptop built in Camera | 30 | 30
PC laptop | Pisee | 5 | 4.9
Mac Mini | Pisee | 0.57 | 0.56
Pishow | Pisee | 4 | 3.5




## Contents
File or directory name | Purpose
---------------------- | -------
src/                   | Source code of all development for this board
INSTALL.md             | Installation instructions for setting up the 'pyshow' board
README.md              | This file

## Blog entries

Relevant blog entries are on [medium.com](medium.com). They are not
public unless they've been incorporated into the Foundry / Cornell
Tech official blog. But they are visible for anyone with the link. The
links to the blog entries (Medium "stories") that are relevant to this
project are listed here.

* [2017-12-17](https://medium.com/p/b800308564a1/) - Background differencing rationale

## disk_images/

SD-Card images of pisee/pishow Linux root partitions

NOTE: The images here are the partitions of `pisee` and `pishow` Raspberry Pi
boards - bit by bit copies, made by the following process:

* Ran the Mac's Applications --> Utilities --> Disk Utility
* Only backed up the partition that has data, not the free space, there
  is a container that has free space included and sums up to the size of
  the card showing up in Disk Utility. That container was not backed up,
  only what shows up inside of it was backed up - that's the partition that
  has the data.

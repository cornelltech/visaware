## disk_images/

SD-Card images of pisee/pishow Linux root partitions

### Notes

The images here are the partitions of `pisee` and `pishow` Raspberry Pi
boards - bit by bit copies, made by the following process (TODO: UPDATE THIS):

* Ran the Mac's Applications --> Utilities --> Disk Utility
* Only backed up the partition that has data, not the free space, there
  is a container that has free space included and sums up to the size of
  the card showing up in Disk Utility. That container was not backed up,
  only what shows up inside of it was backed up - that's the partition that
  has the data.

#### Commands that help:
* On linux use `dmg2img` to convert a dmg file to an img file 
* You can mount the img file as follows:
  * Say your `.img` file is named `FILE.img`
  * Starr with `sudo losetup -f` which prints the next loop device available for use - this will be the argument to the next call - say it returned `/dev/loop?`
  * `sudo losetup /dev/loop? FILE.img` - associates loop device with image
  * `sudo partprobe /dev/loop0` - tells the kernel we have a new loop device
  * `sudo mount /dev/loop0 DIRECTORY` - mounts image at DIRECTORY


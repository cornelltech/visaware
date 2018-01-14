## disk_images/

SD-Card images of pisee/pishow Linux root partitions are no longer stored
in the github directory.

### NOTES

* The Images are for a 32G sd-card or larger.
* There are two images: `pishow.gz` and `pisee.gz` - both contain
  `OpenCV` and `mjpg_streamer` but `pisee.gz` has the camera interface
  enabled while `pishow.gz` has it disabled and `pisee.gz` boots with
  `mjpg_streamer` running in the background and streaming the video on
  `http://localhost:8080/?action=stream`, while `pishow.gz` does not
  stream any video. `pisee.py` image is thus a superset of `pishow.gz`
  image.
* The *pishow* images have the letter *h* written on the sd-card.
* The *pisee* images have the letter *e* written on the sd-card.
* See `/home/pi/sdcard-backup` and `/home/pi/sdcard-restore` for Debian Linux
  based scripts to create sd-card images.

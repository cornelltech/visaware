# Relevant links

Here is where we share any links that are relevant to our work on this project.

* [Raspberry Pi camera bandwidth and quality discussion](https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=136292)
* [picamera documentation](https://picamera.readthedocs.io/en/release-1.13/)
* [Video bandwidth calculations](https://www.mistralsolutions.com/video-surveillance-bandwidth-requirements-calculation-utilization/)
* [mjpg_streamer installation](https://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi)
* [raspicam (C++)](https://github.com/cedricve/raspicam)
* [uv4l installation](http://www.linux-projects.org/uv4l/installation/) - not used for now. Not working after a major attempt.
* [OpenCV installation on Rasperry Pi](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) - this link works for OpenCV v 3.3.1. This is what we used.
* [12 micro SD cards tested with Raspberry Pi](https://www.geek.com/chips/a-geek-tests-12-micro-sd-cards-with-a-raspberry-pi-to-find-the-fastest-1641182/)

### Using OpenCV on pishow
* [Official OpenCV docs](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html)
* [Python example 1](http://petrkout.com/electronics/low-latency-0-4-s-video-streaming-from-raspberry-pi-mjpeg-streamer-opencv/) - this is the main one that shows how to decode a stream using `urllib`
* [Python example 2](https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/)
* [Python example 3](http://www.chioka.in/python-live-video-streaming-example/)

#### CV Processing
* [Background subtraction](https://docs.opencv.org/3.1.0/db/d5c/tutorial_py_bg_subtraction.html) - using `BackgroundSubtractorMOG2`
* [FPS python code](https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/)
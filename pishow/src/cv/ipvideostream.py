# import the necessary packages
from threading import Thread
import cv2

# constant for buffer we hold image data in while streaming from url
BUFFER_LENGTH = 1024

START_MARKER = '\xff\xd8'
END_MARKER = '\xff\xd9'

class WebcamVideoStream:
	def __init__(self, url):
        self.stream = urllib.urlopen(url)
        self.buffer = stream.read(BUFFER_LENGTH)
        self.started = self.buffer.find(START_MARKER)
        self.ended = self.buffer.find(END_MARKER)
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		thread = Thread(target=self.update, args=())
		thread.daemon = True
		thread.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
            self.buffer += stream.read(BUFFER_LENGTH)
            self.started = tmp.find(START_MARKER)
            self.ended = tmp.find(END_MARKER)
            if self.started != -1 and self.ended != -1:
                jpg = self.buffer[image_start:image_end+2]
                # keep leftovers for next iteration
                self.buffer = self.buffer[image_end+2:]
                self.frame = cv2.imdecode(
                    numpy.fromstring(jpg, dtype=numpy.uint8), 1)

			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
self.stopped = True




from threading import Thread


class IpVideoStream:
	def __init__(self, url):
		# initialize the camera and stream
        self.url = url;
        self.buffer = '';
        self.stream = urllib.urlopen(url)
        self.buffer += stream.read(BUFFER_LENGTH)

		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
self.stopped = True

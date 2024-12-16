from engine.require import *
from engine.camera import *





__all__ = ("Recorder",)





class Recorder:
	inst = None
	path = Path("./res/recordings")
	timestamp = None

	font = ImageFont.truetype("./res/fonts/JetBrainsMono/ExtraBold.ttf", round(Data.camera.height / 35))



	# ~~~~~~~~~ Load New File ~~~~~~~~
	@classmethod
	def load(self):
		# Close old writer
		self.close()

		# Get current time
		now = datetime.datetime.now()
		self.timestamp = math.floor(time.time() / (60 ** 2))

		# Generate file path
		path = self.path / f"{now.month}-{now.year}"
		name = f"{now.day}-{now.hour}.avi"

		# Create missing directories
		path.mkdir(
			parents = True,
			exist_ok = True
		)


		# Create file type
		src = cv2.VideoWriter_fourcc(*"XVID")


		# Create file writer
		self.inst = cv2.VideoWriter(
			path / name,
			src,
			Data.camera.fps,
			(
				Data.camera.width,
				Data.camera.height
			)
		)


		# Log file creation
		RFT_Exception(f"Created file {path / name}").print()
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	# ~~~~~~~~~~ Save Frame ~~~~~~~~~~
	@classmethod
	def save(self, frame):
		if (self.inst is not None):
			# Create new file in new hour
			if (self.timestamp != math.floor(time.time() / (60 ** 2))):
				self.load()

		else:
			self.load()

		# Write frame to buffer
		self.inst.write(frame)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	# ~~~~~~~~~~~~~ Close ~~~~~~~~~~~~
	@classmethod
	def close(self):
		if (self.inst is not None):
			# Release open file
			self.inst.release()

		self.inst = None
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	# ~~~~~~~~~~~~ Stylize ~~~~~~~~~~~
	@classmethod
	def stylize(self, frame):
		# Get current time
		now = datetime.datetime.now()

		# Format time
		time_ = now.strftime("%a %I:%M:%S%p").replace(" 0", " ")
		date_ = now.strftime("%m/%d/%y")

		# Get size of strings
		l = self.font.getlength(time_)
		ld = self.font.getlength(date_)
		s = self.font.size

		# Create image canvas
		canvas = Image.new("RGB", [math.ceil(l + 20), (s + 6) * 2], (0, 0, 0))
		draw = ImageDraw.Draw(canvas)

		# Draw time on canvas
		draw.text(
			(
				round((canvas.width - l) / 2),
				2
			),
			time_,
			font = self.font,
			fill = (255, 255, 255)
		)

		# Draw date on canvas
		draw.text(
			(
				round((canvas.width - ld) / 2),
				s + 2
			),
			date_,
			font = self.font,
			fill = (255, 255, 255)
		)


		# Convert to buffer
		arr = np.asarray(canvas)


		# Get bounding area of text
		x, y, w, h = 0, frame.shape[0] - canvas.height, arr.shape[1], arr.shape[0]
		
		# Get frame buffer
		arrFrame = frame[y:y + h, x:x + w]

		# Paste only white pixels onto frame
		arrFrame[:] = np.maximum(arr, arrFrame)

		
		return frame
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


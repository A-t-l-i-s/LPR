from engine.require import *





__all__ = ("Camera",)





class Camera:
	# Camera Instance
	inst = None

	width = None
	height = None
	fps = None

	fpsCurrent = 0
	fpsTime = collections.deque([], 50)


	@classmethod
	def open(self, index:int = 0):
		# Close old camera instance
		self.close()

		try:
			# Load camera
			self.inst = cv2.VideoCapture(index)

			# Set camera properties
			self.inst.set(cv2.CAP_PROP_SETTINGS, 		1)
			self.inst.set(cv2.CAP_PROP_CONVERT_RGB, 	1)
			self.inst.set(cv2.CAP_PROP_AUTOFOCUS, 		int(Data.camera.autofocus))
			self.inst.set(cv2.CAP_PROP_CONTRAST, 		round(Data.camera.contrast * 100))
			self.inst.set(cv2.CAP_PROP_BRIGHTNESS, 		round(Data.camera.brightness * 100))
			self.inst.set(cv2.CAP_PROP_SATURATION, 		round(Data.camera.saturation * 100))
			self.inst.set(cv2.CAP_PROP_HUE, 			round(Data.camera.hue * 100))
			self.inst.set(cv2.CAP_PROP_GAIN, 			round(Data.camera.gain * 100))
			self.inst.set(cv2.CAP_PROP_SHARPNESS, 		round(Data.camera.sharpness * 100))

			# Resolution
			self.inst.set(cv2.CAP_PROP_FRAME_WIDTH, Data.camera.width)
			self.inst.set(cv2.CAP_PROP_FRAME_HEIGHT, Data.camera.height)

			# FPS
			self.inst.set(cv2.CAP_PROP_FPS, Data.camera.fps)


		except:
			# Log failed to load camera
			RFT_Exception(f"Failed to load camera {index}").print()
			RFT_Exception.Traceback().print()
			return False

		else:
			# Log successfully loaded camera
			RFT_Exception(f"Successfully loaded camera {index}").print()
			return True



	@classmethod
	def read(self):
		# ~~~~~~~~~~~~~~ FPS ~~~~~~~~~~~~~
		# Append current time to timestamps
		self.fpsTime.append(time.time())

		# Get amount of timestamps
		l = len(self.fpsTime)

		if (l > 1):
			# Get first and last timestamp
			last = self.fpsTime[-1]
			first = self.fpsTime[0]

			# Get difference between timestamps
			self.fpsCurrent = l / (last - first)


		if (abs(self.fpsCurrent - Data.camera.fps) > 10):
			if (len(self.fpsTime) == 50):
				RFT_Exception(f"Program is falling behind at {round(self.fpsCurrent)} fps", RFT_Exception.WARNING).print()
		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		if (self.inst is not None):
			return self.inst.read()

		else:
			return False, None



	@classmethod
	def close(self):
		if (self.inst is not None):
			# Close camera instance
			self.inst.release()

			# Log closed camera
			RFT_Exception("Camera closed").print()
		
		self.inst = None






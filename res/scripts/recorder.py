from engine.require import *
from engine.camera import *
from engine.recorder import *





if (__name__ == "__main__"):
	Camera.open()

	while True:
		result, frame = Camera.read()

		if (result):
			frame = Recorder.stylize(frame)
			Recorder.save(frame)




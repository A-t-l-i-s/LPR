from engine.require import *
from engine.camera import *
from engine.server import *
from engine.recorder import *





if (__name__ == "__main__"):
	Camera.open(0)
	Server.run()



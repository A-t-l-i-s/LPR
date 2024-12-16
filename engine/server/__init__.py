from engine.require import *
from engine.camera import *
from engine.recorder import *





__all__ = ("Server",)





class Server(RFT_Object):
	@classmethod
	def run(self):
		# Initialize flask app
		self.app = Flask(
			"LPR",
			static_folder = "./res/static",
			template_folder = "./res/templates"
		)


		# Index
		@self.app.route("/")
		def index():
			return FlaskTemplate("index.html")


		# Feed
		@self.app.route("/feed")
		def feed():
			return FlaskResponse(
				self.stream(),
				mimetype = "multipart/x-mixed-replace; boundary=frame"
			)


		# Log server hosting
		RFT_Exception(f"Hosting on http://{Data.server.host.strip('/')}:{Data.server.port}/").print()

		if (Data.server.production):
			# Run app in a production server
			waitress.serve(
				self.app,
				host = Data.server.host,
				port = Data.server.port,
				threads = 4
			)

		else:
			# Run app in a development server
			self.app.run(
				host = Data.server.host,
				port = Data.server.port,
				debug = True,
				threaded = True,
				use_reloader = False
			)



	@classmethod
	def stream(self):
		while True:
			success, frame = Camera.read()

			if (success):
				frame = Recorder.stylize(frame)

				ret, buffer = cv2.imencode(".jpg", frame)
				buf = buffer.tobytes()

				yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf + b"\r\n")

			else:
				break




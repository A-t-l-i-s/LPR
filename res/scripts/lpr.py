from engine.require import *



cam = cv2.VideoCapture(1)



while True:
	status, frame = cam.read()

	if (status):
		# Timestamp
		timestamp = time.time()
		
		# Convert to grayscale image
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.bilateralFilter(gray, 11, 17, 17)

		# Get outlines
		outlines = cv2.Canny(gray, 30, 200)


		contours = cv2.findContours(outlines.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]


		for c in contours:
			p = cv2.arcLength(c, True)
			a = cv2.approxPolyDP(c, 0.018 * p, True)
			
			if (len(a) == 4):
				x, y, w, h = cv2.boundingRect(a)
				plate = frame[y:y + h, x:x + w]

				cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

				plate = cv2.resize(plate, (round((frame.shape[1] / w) * w), round((frame.shape[0] / h) * h)))
				cv2.imshow("Plate", plate)
				
				text = pytesseract.image_to_string(plate, config = f"--psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[]{{}}|;\':\",./<>?").strip()

				if (text):
					name = ""
					allowed = string.ascii_letters + string.digits

					for v in text:
						if (v in allowed):
							name += v

						else:
							name += "_"
					
					if (name):
						t = Tables[name]

						if (not t.contains("events")):
							t.events = []
						
						t.events.append({
							"text": text,
							"timestamp": timestamp
						})

						Tables_Obj.saveAll()

				break


		cv2.imshow("Frame", frame)
		cv2.waitKey(1)



cam.release()


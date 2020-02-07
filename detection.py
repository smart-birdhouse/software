# Libraries
import pir
import ultrasonic
import microphone
from time import sleep, localtime, strftime
from signal import signal, SIGINT
from RPi import GPIO

import picamera

class Detector:
	def __init__(self):
		self.u = ultrasonic.Ultrasonic()
		self.p = pir.PIR()

		self.statusFile = open("birdlog.txt", 'a')
		self._statusWrite("on")
		self.birdHere == 0

	def startDetection(self):

		signal(SIGINT, self._handler)

		self._statusWrite("start")

		# startup delay for sake of pir stabilization
		sleep(2)

		dist = 20
		motion = 0
		counter = 0
		birdHere = 0


		while True:
			try:
				dist = self.u.distance
				motion = self.p.movement

				if( dist <= 12 and motion == 1 and self.birdHere == 0 ):
					self._statusWrite("in")
					print("bird in")
					birdHere = 1
					sleep(1)

				elif( (dist <= 12 or motion == 1) and self.birdHere == 1 and counter >= 20):
					self._statusWrite("here")
					print("bird still here")
					counter = 0

				elif( self.birdHere == 1 and dist > 12 and motion == 0 ):
					self._statusWrite("out")
					print("bird out")
					birdHere = 0

			except RuntimeError:
				print("Polling error")

			if self.birdHere:
				counter += 1
				sleep(1)
			sleep(0.2)


	def _statusWrite(self, statusType):
		timeStatus = strftime('%H:%M:%S %m/%d/%y')

		if(statusType == "on"):
			self.statusFile.write("Program Start: " + timeStatus + "\n")

		elif(statusType == "start"):
			self.statusFile.write("Detection Start: " + timeStatus + "\n")

		elif(statusType == "in"):
			self.statusFile.write("Bird in: " + timeStatus + "\n")

		elif(statusType == "here"):
			self.statusFile.write("Bird still here: " + timeStatus + "\n")

		elif(statusType == "out"):
			self.statusFile.write("Bird has left: " + timeStatus + "\n")

		elif(statusType == "done"):
			self.statusFile.write("Program close: " + timeStatus + "\n\n")


	def _handler(self, signal_recieved, frame):
		print("Measurement stopped by user.")
		self.u.deinit()
		self.p.sleep()
		GPIO.cleanup()
		self._statusWrite("done")
		self.statusFile.close()
		exit(0)


if __name__ == '__main__':
	det = Detector()
	det.startDetection()

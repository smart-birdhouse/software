import pir
import ultrasonic

from time import sleep, strftime
from signal import signal, SIGINT
from RPi import GPIO

class Detector:
	"""
	Detection class. Initializes pir and ultrasonic objects.
	"""

	def __init__(self, logfile = "birdlog.txt"):
		self.u = ultrasonic.Ultrasonic()
		self.p = pir.PIR()

		self.statusFile = open(logfile, 'a')
		self._statusWrite("on")
		self.birdHere = 0

		signal(SIGINT, self._handler)

	def startDetection(self, detectDist = 12, noBirdUpdateFreq = 5, birdUpdateFreq = 1):
		"""
		Infinite loop to check for bird using ultrasonic and pir.
		Writes to log file on status change.
		"""

		self._statusWrite("start")

		# startup delay for sake of pir stabilization
		sleep(2)

		dist = detectDist+1
		motion = 0
		counter = 0
		self.birdHere = 0


		while True:
			try:
				dist = self.u.distance
				motion = self.p.movement

				if( dist <= detectDist and motion == 1 and self.birdHere == 0 ):
					self._statusWrite("in")
					self.birdHere = 1
					sleep(1)

				elif( (dist <= detectDist or motion == 1) and self.birdHere == 1 and counter >= 20):
					self._statusWrite("here")
					counter = 0

				elif( self.birdHere == 1 and dist > detectDist and motion == 0 ):
					self._statusWrite("out")
					self.birdHere = 0

			except RuntimeError:
				print("Polling error")

			if self.birdHere:
				counter += 1
				sleep(1/birdUpdateFreq)

			else:
				sleep(1/noBirdUpdateFreq)


	def _statusWrite(self, statusType):
		"""Append status to statusfile with timestamp"""

		timeStatus = strftime('%H:%M:%S %m/%d/%y')

		statusDict = {
			"on":"\nProgram start: ",
			"start":"Detection start: ",
			"in":"Bird in: ",
			"here":"Bird still here: ",
			"out":"Bird has left:",
			"done":"Program close: "
		}

		self.statusFile.write(statusDict[statusType] + timeStatus + "\n")


	def _handler(self, signal_recieved, frame):
		"""
		Deinitializes sensors, closes log file, runs cleanup,
		and closes on keyboard interrupt
		"""
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

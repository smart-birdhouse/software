# Libraries
import pir
import ultrasonic
from time import sleep, localtime
from signal import signal, SIGINT

import picamera


# "h:m:s m/d/y", used for status writes
def timeStrStatus():
	return ( str(localtime().tm_hour) + ':' + str(localtime().tm_min) +
		':' + str(localtime().tm_sec) + ' ' +  str(localtime().tm_mon) + '/' +
		str(localtime().tm_mday) + '/' + str(localtime().tm_year) )

# "ymdhms", used for easily sortable filename writes
def timeStrSort():
	return ( str(localtime().tm_year) + str(localtime().tm_mon) +
			str(localtime().tm_mday) + str(localtime().tm_hour) + str(localtime().tm_min) +
			str(localtime().tm_sec) )

def handler0():
	print("Measurement stopped by user.")
	u.deinit()
	p.sleep()
	GPIO.cleanup()
	statusFile.write("Program Stop: " + timeStringStatus() + '\n')
	statusFile.close()
	#camera.stop_recording()
	exit(0)


if __name__ == '__main__':

	u = ultrasonic.Ultrasonic()
	p = pir.PIR()

	signal(SIGINT, handler0)

	statusFile = open("statushistory.txt", 'a')
	statusFile.write("Program Start: " + timeStrStatus() + '\n')

	#camera = picamera.PiCamera()
	#camera.resolution = (1280, 720)

	try:
		dist = u.distance
		oldMotion = p.movement
	except RuntimeError:
		dist = 10
		oldMotion = 1
		newMotion = 1

	counter = 0
	birdHere = 0

	while True:
		try:
			dist = u.distance
			newMotion = p.movement

			if( dist <= 10 and newMotion == 1 and oldMotion == 0 ):
				statusFile.write("Bird in: " + timeStrStatus() + '\n')
				birdHere = 1
				#camera.start_recording("video" + timeStrSort() + ".h264")
				#camera.wait_recording(5)
				#camera.stop_recording()

			elif( dist <= 10 and newMotion == 0 and birdHere == 1 and counter == 10):
				statusFile.write("Bird still here: " + timeStrStatus() + '\n')
				counter = 0

			elif( birdHere == 1 and dist > 10 ):
				statusFile.write("Bird has left: " + timeStrStatus() + '\n')
				birdHere = 0

		except RuntimeError:
			print("Polling error")

		oldMotion = newMotion
		counter += 1
		sleep(0.2)


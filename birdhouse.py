# Libraries
import pir
import ultrasonic
from time import sleep, localtime
from signal import signal, SIGINT
from RPi import GPIO

import picamera


# "h:m:s m/d/y", used for status writes
def timeStrStatus():
	return ( str(localtime().tm_hour) + ':' + str(localtime().tm_min) +
		':' + str(localtime().tm_sec) + ' ' +  str(localtime().tm_mon) + '/' +
		str(localtime().tm_mday) + '/' + str(localtime().tm_year) )

# "ymdhms", used for easily sortable filename writes
def timeStrSort():
	return ( str(localtime().tm_year) + "_" + str(localtime().tm_mon) + "_" +
			str(localtime().tm_mday) + "_" + str(localtime().tm_hour) + "_" +
			str(localtime().tm_min) + "_" + str(localtime().tm_sec) )

def handler(signal_recieved, frame):
	print("Measurement stopped by user.")
	u.deinit()
	p.sleep()
	GPIO.cleanup()
	statusFile.write("Program Stop: " + timeStrStatus() + "\n\n")
	statusFile.close()
	camera.close()
	exit(0)


if __name__ == '__main__':

	u = ultrasonic.Ultrasonic()
	p = pir.PIR()

	signal(SIGINT, handler)

	statusFile = open("birdlog.txt", 'a')
	statusFile.write("Program Start: " + timeStrStatus() + "\n")

	camera = picamera.PiCamera()
	camera.resolution = (3280, 2464)
	# camera.framerate = 15

	try:
		dist = u.distance
		motion = p.movement
	except RuntimeError:
		dist = 20
		motion = 0

	counter = 0
	birdHere = 0

	# startup delay for sake of pir stabilization
	sleep(2)

	while True:
		try:
			dist = u.distance
			motion = p.movement

			if( dist <= 12 and motion == 1 and birdHere == 0 ):
				statusFile.write("Bird in: " + timeStrStatus() + '\n')
				print("bird in")
				birdHere = 1
				camera.start_preview()
				sleep(2)
				camera.capture("pic" + timeStrSort() + ".jpg")
				camera.stop_preview()
				# camera.wait_recording(5)
				# camera.stop_recording()

			elif( (dist <= 12 or motion == 1) and birdHere == 1 and counter >= 20):
				statusFile.write("Bird still here: " + timeStrStatus() + '\n')
				print("bird still here")
				counter = 0

			elif( birdHere == 1 and dist > 12 and motion == 0 ):
				statusFile.write("Bird has left: " + timeStrStatus() + '\n')
				print("bird out")
				birdHere = 0


		except RuntimeError:
			print("Polling error")

		if birdHere:
			counter += 1
			sleep(1)
		sleep(0.2)

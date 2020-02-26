import pir
import ultrasonic

from time import sleep, strftime
from signal import signal, SIGINT
from RPi import GPIO

class Detector:
    """Detection class. Initializes pir and ultrasonic objects.
    After init and starting detection, check if there is a bird detected by
    checking the value of the birdHere variable. It is updated based on an 
    interrupt from the PIR input"""


    def __init__(self, detectDist = 12):
        self.u = ultrasonic.Ultrasonic()
        self.p = pir.PIR()

        self.birdHere = 0
        self.detectDist = detectDist

        self.statusWrite("on")

    def isBirdHere(self):
        return self.birdHere

    def startDetection(self):
        """Runs detection in the background based around the PIR interrupt. 
        Whenever the PIR interrupt is triggered, it runs the _birdUpdateHandler() function"""

        self.statusWrite("start")

        # get initial bird status
        if(self.p.movement == 1):
            print("Motion detected")
            self._distanceCheck()

        # change interrupt handler for pir input pin to the _birdUpdateHandler() function
        # this enables us to update birdHere in the background using the pin interrupt
        self.p.newHandler(self._birdUpdateHandler)

    def stopDetection(self):
        """Disables PIR interrupt, which will pause detection"""
        self.statusWrite("stop")
        self.p.sleep()
        self.birdHere = 0

    def _distanceCheck(self):
        """Checks whether there is an object in distance less than the 
        detectDist threshold with data smoothing and updates birdHere and logs to the 
        status file accordingly"""

        # Catches the occasional polling error that occurs with the ultrasonic distance sensor
        try:
            # 3 point averager to smooth out distance data
            dist = self.u.distance
            sleep(0.05)
            dist += self.u.distance
            sleep(0.05)
            dist += self.u.distance
            dist = dist/3

            print("Distance check reading: {0:1.3f}".format(dist))

            if( dist <= self.detectDist ):
                if( self.birdHere == 0 ):
                    self.statusWrite("in")
                self.birdHere = 1

            else:
                if( self.birdHere == 1 ):
                    self.statusWrite("out")
                self.birdHere = 0

        except RuntimeError:
            pass


    def _birdUpdateHandler(self, pin):
        """Handler called on PIR input change. While motion is detected, it will check for bird presence until
        bird is detected or until timeout"""

        # Update movement value from PIR pin status
        self.p.update(pin)

        if(self.p.movement == 1):
            print("Motion detected")
            self._distanceCheck()

            timeout = 0
            while(self.birdHere == 0 and self.p.movement == 1 and timeout < 15):
                sleep(1)
                self._distanceCheck()
                timeout += 1

        else:
            print("Motion ended")
            self.birdHere = 0

    def statusWrite(self, statusType):
        """Append status to statusfile with timestamp"""

        timeStatus = strftime('%H:%M:%S %m/%d/%y')

        # dict used for ease of writing
        statusDict = {
            "on":"\nProgram start: ",
            "start":"Detection start: ",
            "stop":"Detection stop: ",
            "in":"Bird in: ",
            "here":"Bird still here: ",
            "out":"Bird has left: ",
            "done":"Program close: "
        }

        with open("birdlog.txt",'a') as statusFile:
            statusFile.write(statusDict[statusType] + timeStatus + "\n")

    def __del__(self):
        """Runs cleanup and closes"""
        self.p.sleep()
        GPIO.cleanup()



def handler(signal_received, frame):
    print("Measurement stopped by user.")
    det.u.deinit()
    exit(0)


if __name__ == '__main__':

    det = Detector()

    det.startDetection()

    signal(SIGINT, handler)

    while(1):
        sleep(2)
        if(det.isBirdHere()):
            print("Bird is here")
        else:
            print("Bird is not here")

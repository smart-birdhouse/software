import detection
import audio_video
import environment

from signal import signal, SIGINT
from time import sleep

def handler(sigal_received, frame):
    print("Measurement stopped by user.")
    det.stopDetection()
    av.mic.stop()
    av.cam.stop()
    exit(0)


if __name__ == '__main__':

    det = detection.Detector()
    av = audio_video.AudioVideo()
    det.startDetection()
    e = environment.Environment()

    signal(SIGINT, handler)

    oldStatus = 0
    status = 0
    timeout = 0
    timeToTimeout = 20
    sleep(0.5)

    while(1):
        status = det.isBirdHere()

        if status and (not oldStatus):
            print("Bird cometh")
            av.startRecording()
            timeout = 0

        elif status and oldStatus and timeout<timeToTimeout:
            print("here and timing")
            timeout+=1

        elif (not status) and oldStatus:
            print("Bird goeth")
            if timeout < timeToTimeout:
                av.stopRecording()
                timeout = timeToTimeout+1
                print("bird left before timeout")

        elif timeout == timeToTimeout:
            timeout+=1
            av.stopRecording()
            print("timeout")


        oldStatus = status
        sleep(0.5)

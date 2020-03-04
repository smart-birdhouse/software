#import microphone
from microphone import Microphone
from camera import Camera
import detection
#from time import sleep
import time
#import detection
from _thread import start_new_thread
from signal import signal, SIGINT
#from time import time
import ffmpeg

class AudioVideo:
    """
    Audio/Video class. Combines motion detection with recording
    of audio and video, then stitches together .h264 video with
    .wav audio to make .mp4 video
    """
    def __init__(self):
        self.mic = Microphone()
        self.cam = Camera() 

    def startRecording(self):
        self.start_time = time.time()
        self.mic.start()
        self.cam.stop() 
        self.cam.start()

    def stopRecording(self):
        self.mic.stop()
        self.cam.stop()
        print("Recording stops.")    
        print("--- %s seconds ---" % (time.time() - self.start_time))           

def handler(signal_received, frame):
    print("Measurement stopped by user.")
    av.mic.stop()
    av.cam.stop()
    exit(0)

if __name__ == '__main__':
    av = AudioVideo()
    signal(SIGINT, handler)
    print("Starting run...")
    av.startRecording()
    time.sleep(10)
    av.stopRecording()
    print("Ended run.")


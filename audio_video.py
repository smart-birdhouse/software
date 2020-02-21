#import microphone
from microphone import Microphone
#import camera
import detection
#from time import sleep
import time
#import detection
from _thread import start_new_thread
from signal import signal, SIGINT
#from time import time

class AudioVideo:
    """
    Audio/Video class. Combines motion detection with recording
    of audio and video, then stitches together .h264 video with
    .wav audio to make .mp4 video
    """

    def start(self):
        mic = Microphone()
        #cam = Camera(filename = tempVideo.h264)

        d = detection.Detector()
        d.startDetection()
        flag = 1
        while flag == 1:
            #if(motion == detected)
            if d.isBirdHere() == 1:    # motion is detected
                # when motion is detected
                print("Motion detected, starting recording")
                start_time = time.time()
                #print("mic start")
                #mic.start(filename = 'tempAudio.wav') # 30 second recording
                #cam.start()
                flag = 0
            else:
                time.sleep(2)    # don't spend too much processing power checking

                
        time.sleep(10)   # record a minimum of audio and video
        
        counter = 0

        print("Recording stops.")    
        print("--- %s seconds ---" % (time.time() - start_time))           
        #mic.stop()
        #cam.stop()

        
        # convert .h264 to .mp4 - might not have to do
        # https://stackoverflow.com/questions/45040261/python-3-auto-conversion-from-h264-to-mp4
##        from subprocess import CalledProcessError
##        command = shlex.split("MP4Box -add {} {}.mp4".format(tempVideo.h264)
##        try:
##            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
##        except CalledProcessError as e:
##            print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

        #completedVideoFilename = strftime("%m%d%Y-%H%M%S")+'.mov'
        
        # merge .mp4 and .wav to .mov
        #avconv -v debug -i tempAudio.wav -i tempVideo.mp4 -c:a libmp3lame -qscale 20 -shortest output.mov
##        avconv -v debug -i tempAudio.wav -i tempVideo.mp4 -c:a libmp3lame -qscale 20 -shortest completedVideoFilename
        
        print("Final video stored as completedVideoFilename")

def handler(signal_received, frame):
    print("Measurement stopped by user.")
    #av.mic.stop()
    #av.cam.stop()
    exit(0)

if __name__ == '__main__':
    av = AudioVideo()
    signal(SIGINT, handler)
    print("Starting run...")
    av.start()
    print("Ended run.")


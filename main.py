"""
Top level program for running detection with event recording.
"""
import detection
import audio_video
import environment

    def handler(sigal_received, frame):
        print("Measurement stopped by user.")
        det.stopDetection()
        av.mic.stop()
        av.cam.stop()
        exit(0)


    det = detection.Detector()
    av = audio_video.AudioVideo()
    det.startDetection()
    e = environment.Environment()

    signal(SIGINT, handler)
    stats = jsonParser()
    detectTime = ""
    oldStatus = 0
    status = 0
    timeout = 0
    timeToTimeout = 20
    
    #sleep((shared_time_delay.value)/1000)
    sleep(5);
    shared_bird_detected.value = 1
    status = 1
    
    while(1):
        #shared_bird_detected.value = det.isBirdHere()
        #status = shared_bird_detected.value
        if status and (not oldStatus):
            print("Bird cometh")
            av.startRecording()
            timeout = 0
            shared_bird_detected.value = 1
            shared_timespec.value = datetime.datetime.timestamp(datetime.datetime.now())
            #date = datetime.datetime.now()
            detectTime = (datetime.datetime.now()).strftime("%d-%m-%y_%H:%M")
            stats.createJSON(detectTime)

        elif status and oldStatus and timeout<timeToTimeout:
            print("here and timing")
            timeout+=1
            shared_timespec.value = datetime.datetime.timestamp(datetime.datetime.now())
            stats.updateJSON(detectTime)

        elif (not status) and oldStatus:
            print("Bird goeth")
            shared_bird_detected.value = 0 
            if timeout < timeToTimeout:
                av.stopRecording()
                timeout = timeToTimeout+1
                print("bird left before timeout")
            shared_timespec.value = datetime.datetime.timestamp(datetime.datetime.now())
            stats.updateJSON(detectTime)

        elif timeout == timeToTimeout:
            timeout+=1
            av.stopRecording()
            print("timeout")

        #print(timeout)
        oldStatus = status
        #sleep(int(shared_time_delay.value))
        if timeout >= timeToTimeout:
            status=0
        sleep(1)
        

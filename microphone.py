from subprocess import Popen
from time import strftime


class Microphone:
    _BASE_COMMAND = ['arecord', '-D plughw:1', '-c1',
                     '-r 48000', '-f S32_LE', '-t wav', '-V mono']

    RECORDING = 'recording'
    DONE = 'done'
    STOPPED = 'stopped'
    IDLE = 'idle'

    def __init__(self, filename=strftime("%m%d%Y-%H%M%S")+'.wav'):
        self._filename = filename
        self._process = None

    def start(self, duration=None):
        if(self._process is None or self._process.poll() is None):
            command = self._BASE_COMMAND
            if(duration):
                command.append(f'-d {duration}')

            command.append(self._filename)

            self._process = Popen(command)

    def stop(self):
        if(self.p is not None):
            self._process.terminate()

    def status(self):
        if(self._process is None):
            return self.IDLE
        elif(self._process.poll() is None):
            return self.RECORDING
        elif(self._process.poll() < 0):
            return self.STOPPED
        else:
            return self.DONE


if __name__ == '__main__':
    mic = Microphone()

    print(f"Microphone current status: {mic.status()}")
    print(f"Starting 5 second recording..")
    mic.start(duration=5)
    print(f"Microphone current status: {mic.status()}")

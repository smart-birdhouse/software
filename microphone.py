"""Utilizes Adafruit I2S MEMS Microphone to create a sound file.

More info: https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout
"""

from subprocess import Popen
from time import strftime, sleep


class Microphone:
    """Class setup to use the Adafruit I2S MEMS Microphone."""
    _BASE_COMMAND = "arecord -D plughw:1 -c1 -r 48000 -f S32_LE -t wav -V mono".split(
        ' ')

    RECORDING = 'recording'
    DONE = 'done'
    STOPPED = 'stopped'
    IDLE = 'idle'

    def __init__(self):
        """Creates a new Microphone object."""
        self._process = None

    def start(self, duration=None, filename=strftime("%m%d%Y-%H%M%S")+'.wav'):
        """Begins a recording.

        Opens a process to begin a microphone recording.

        Args:
            duration: A duration for the recording to last. If None, will continue infinitely
            filename: A filename to use for the wav file, uses the time in MMDDYYYY-HHMMSS format by default.
        """

        if(self._process is None or self._process.poll() is None):
            command = self._BASE_COMMAND
            if(duration):
                command.append(f'-d {duration}')

            command.append("/home/Trent/software/app/audio/"+filename)

            print(f"command= {command}")
            self._process = Popen(command)

    def stop(self):
        """Stops an ongoing recording."""
        if(self._process is not None):
            self._process.terminate()
            self._process = None

    def status(self):
        """Returns the status of the microphone.

        Returns:
            A string describing the current state of the microphone.
            one of: 'recording', 'done', 'stopped', 'idle'.

            Microphone also contains constants for ease of use:
            RECORDING, DONE, STOPPED, IDLE.
        """

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
    mic.start()
    print(f"Microphone current status: {mic.status()}")
    sleep(5)
    mic.stop()
    print(f"Microphone current status: {mic.status()}")

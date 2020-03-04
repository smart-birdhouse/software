"""Utilizes UV4L and the Raspberry Pi Camera Module V2 to record a video file.

More info: https://www.linux-projects.org/uv4l/installation/
"""

from subprocess import Popen
from time import strftime, sleep


class Camera:
    """Class setup to use the UV4L library to record video."""
    _CONFIG = """v4l2-ctl --set-fmt-video=width=1920,height=1080,pixelformat="H264" -d /dev/video0; sudo chrt -a -r -p 99 `pgrep uv4l`"""
    _START_RECORD = 'dd if=/dev/video0 bs=1M'.split(' ')

    RECORDING = 'recording'
    DONE = 'done'
    STOPPED = 'stopped'
    IDLE = 'idle'

    def __init__(self):
        """Creates a new Camera object."""
        self._process = None

    def start(self, duration=None, filename=strftime("%m%d%Y-%H%M%S")+'.h264'):
        """Begins a recording.

        Opens a process to begin a camera recording.

        Args:
            duration: A duration for the recording to last. If None, will continue infinitely
            filename: A filename to use for the video file, uses the time in MMDDYYYY-HHMMSS format by default.
        """

        if(self._process is None or self._process.poll() is None):
            command = self._START_RECORD

            command.append(f'of={filename}')

            self._process = Popen(command)  # , shell=True)

            if(duration):
                sleep(duration)
                self._process.terminate()
        else:
            raise Exception(
                "Tried to start a video while one is already running!")

    def stop(self):
        """Stops an ongoing recording."""
        if(self._process is not None):
            self._process.terminate()

    def status(self):
        """Returns the status of the camera.

        Returns:
            A string describing the current state of the camera.
            one of: 'recording', 'done', 'stopped', 'idle'.

            Camera also contains constants for ease of use:
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
    cam = Camera()

    print(f"Camera current status: {cam.status()}")
    print(f"Starting 5 second recording..")
    cam.start(filename='unittest.h264', duration=5)
    print(f"Camera current status: {cam.status()}")

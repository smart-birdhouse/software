"""Utilizes HCSR04 Ultrasonic Distance sensor to measure distance.

More info: https://learn.adafruit.com/ultrasonic-sonar-distance-sensors
"""

from board import D23, D24
from adafruit_hcsr04 import HCSR04
from time import sleep
from signal import signal, SIGINT


class Ultrasonic(HCSR04):
    """Small wrapper for Adafruit HCSR04 class."""

    def __init__(self):
        """Calls the HCSR04 initialization using the proper trigger and echo pins."""
        super().__init__(trigger_pin=D24, echo_pin=D23)


def handler(signal_received, frame):
    """Function linked with signal to SIGINT so that we can cleanup when the user presses Ctrl-C."""
    print("Measurement stopped by user.")
    u.deinit()
    exit(0)


if __name__ == '__main__':
    u = Ultrasonic()
    signal(SIGINT, handler)

    while True:
        try:
            print(u.distance)
        except RuntimeError:
            print("Retrying!")
        sleep(0.2)

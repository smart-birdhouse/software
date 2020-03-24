# Libraries
from board import D23, D24
import adafruit_hcsr04
from time import sleep
from signal import signal, SIGINT


class Ultrasonic(adafruit_hcsr04.HCSR04):
    def __init__(self, usePulse = False):
        adafruit_hcsr04._USE_PULSEIO = usePulse
        super().__init__(trigger_pin=D24, echo_pin=D23)


def handler(signal_received, frame):
    print("Measurement stopped by user.")
    u.deinit()
    exit(0)


if __name__ == '__main__':
    u = Ultrasonic(usePulse = True)
    signal(SIGINT, handler)

    while True:
        try:
            print(u.distance)
        except RuntimeError:
            print("Retrying!")
        sleep(0.5)

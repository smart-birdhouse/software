# Libraries
from board import D23, D24
from adafruit_hcsr04 import HCSR04
from time import sleep
from signal import signal, SIGINT


class Ultrasonic(HCSR04):
    def __init__(self):
        super().__init__(trigger_pin=D24, echo_pin=D23)


def handler():
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
        sleep(0.1)

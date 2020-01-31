# Libraries
from board import D5, D6
from adafruit_hcsr04 import HCSR04
from time import sleep


class Ultrasonic(HCSR04):
    def __init__(self):
        super().__init__(trigger_pin=D5, echo_pin=D6)


if __name__ == '__main__':
    u = Ultrasonic()
    try:
        while True:
            try:
                print(u.distance)
            except RuntimeError:
                print("Retrying!")
            sleep(0.1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        u.deinit()

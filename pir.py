# from https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/circuitpython-code

from board import D2
import GPIO
from signal import signal, SIGINT


class PIR:
    def __init__(self, pin=D2):
        self._pin = pin  # pin number connected to PIR sensor output wire.

        # set as input
        GPIO.setup(self._pin, GPIO.IN)

        # set initial value
        self.movement = GPIO.input(pin)

        # add a rising edge detection that sets the movement variable to input on the pin
        # callbacks are threaded, meaning this does not interrupt main program execution
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=self._handler)

    def _handler(self):
        self.movement = GPIO.input(self._pin)

    def sleep(self):
        # remove detection so the handler is no longer called
        GPIO.remove_event_detect(self._pin)

    def wake(self):
        # re-add event detection
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=self._handler)


def handler(signal_received, frame):
    print("Measurement stopped by user.")
    p.sleep()
    GPIO.cleanup()
    exit(0)


if __name__ == '__main__':
    p = PIR()
    signal(SIGINT, handler)

    while True:
        pir_value = p.movement
        if pir_value:
            # PIR is detecting movement! Turn on LED.
            led.value = True
            # Check if this is the first time movement was
            # detected and print a message!
            if not old_value:
                print('Motion detected!')
        else:
            # PIR is not detecting movement. Turn off LED.
            led.value = False
            # Again check if this is the first time movement
            # stopped and print a message.
            if old_value:
                print('Motion ended!')

        old_value = pir_value

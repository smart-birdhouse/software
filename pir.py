# from https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/circuitpython-code

from RPi import GPIO
from signal import signal, SIGINT
from board import D2


class PIR:
    def __init__(self):
        self._pin = 5 # pin number connected to PIR sensor output wire

		# set as input
        GPIO.setup(self._pin, GPIO.IN)

        # set initial value
        self.movement = GPIO.input(self._pin)

        # add a rising edge detection that sets the movement variable to input on the pin
        # callbacks are threaded, meaning this does not interrupt main program execution
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=self._handler)

    def _handler(self, pin):
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

    old_value = p.movement
    print(old_value)
    while True:
        pir_value = p.movement
        if pir_value:
            # Check if this is the first time movement was
            # detected and print a message!
            if not old_value:
                print('Motion detected!')
        else:
            # Again check if this is the first time movement
            # stopped and print a message.
            if old_value:
                print('Motion ended!')

        old_value = pir_value

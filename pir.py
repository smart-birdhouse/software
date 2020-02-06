"""Utilizes Adafruit Passive Infrared sensor to detect motion.

More info: https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/circuitpython-code
"""

from board import D2
from RPi import GPIO
from signal import signal, SIGINT
from board import D5

class PIR:
    """Class setup to use the Adafruit Passive Infrared sensor.

    Uses GPIO event detection to link the movement attribute to the appropriate pin.

    Attributes:
        movement: Indicates the status of the data pin, turns to 1 if there is movement.

    """

    def __init__(self):
        """Creates a new PIR object.

        Uses the correct pin number and GPIO functions to setup input pin and event detection.
        """
        self._pin = 2  # pin number connected to PIR sensor output wire

        # set as input
        GPIO.setup(self._pin, GPIO.IN)

        # set initial value
        self.movement = GPIO.input(self._pin)

        # add a rising edge detection that sets the movement variable to input on the pin
        # callbacks are threaded, meaning this does not interrupt main program execution
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                                    callback=self._handler0)

    def _handler0(self):
        """
        Updates 'movement' on pin change
        """
        self.movement = GPIO.input(self._pin)

    def sleep(self):
        """
        Remove detection so the handler is no longer called.
        """
        GPIO.remove_event_detect(self._pin)

    def wake(self):
        """
        Restart the detection handler
        """
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                                    callback=self._handler)


def handler(signal_received, frame):
    """Function linked with signal to SIGINT so that we can cleanup when the user presses Ctrl-C."""
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

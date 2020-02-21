from RPi import GPIO
from signal import signal, SIGINT
from board import D5
from time import sleep

class PIR:
    """
    Class defining operations for the PIR sensor.
    After init, get the current state of the PIR through the class variable 'movement' which is
    updated on an interrupt from a change in the pin state.
    """

    def __init__(self):
        """Starts detection on initialization"""

        self._pin = 5  # pin number connected to PIR sensor output wire

        # set as input
        GPIO.setup(self._pin, GPIO.IN)

        # set initial value, with wait for stabilization
        sleep(0.5)
        self.movement = GPIO.input(self._pin)

        # add a rising edge detection that sets the movement variable to input on the pin
        # callbacks are threaded, meaning this does not interrupt main program execution
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=self._callback)

    def _callback(self, pin):
        """Private callback to update 'movement' on pin change"""
        self.update(pin)

    def update(self, pin):
        """Public function to access movement updating for use with custom handler"""
        self.movement = GPIO.input(pin)

    def sleep(self):
        """Remove detection so the handler is no longer called."""
        GPIO.remove_event_detect(self._pin)

    def wake(self):
        """Restart the detection handler"""
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=self._callback)

    def newHandler(self, func):
        """Changes the function called when detecting the pir data event

        Args:
            func: the function to be used
        """
        self.sleep()
        GPIO.add_event_detect(self._pin, GPIO.BOTH,
                              callback=func)


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
        sleep(0.2)

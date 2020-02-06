"""Contains functions used to save power."""

from subprocess import Popen


def enable_power_save():
    """ Turns off USB and HDMI to save power,
    MAKE SURE TO CALL disable_power_save() to re-enable! """
    process = Popen(  # turns off USB
        "echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind", shell=True)
    process.wait()

    # turns off HDMI
    Popen("sudo /opt/vc/bin/tvservice -o", shell=True)


def disable_power_save():
    """ Turns back on USB and HDMI """
    process = Popen(  # turns on USB
        "echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind", shell=True)
    process.wait()

    # turns on HDMI
    Popen("sudo /opt/vc/bin/tvservice -p", shell=True)

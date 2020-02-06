"""Utilizes Adafruit BME280 to monitor the temperature, humidity, pressure, and altitude.

More info: https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/overview
"""
from board import SCL, SDA
from busio import I2C
from adafruit_bme280 import Adafruit_BME280_I2C
from time import sleep


class Environment(Adafruit_BME280_I2C):
    """Small wrapper for Adafruit_BME280_I2C class that handles initialization ports."""

    SEA_LEVEL_PRESSURE = 1018.9

    def __init__(self):
        """Use the Adafruit_BME280_I2C initialization with default I2C ports."""
        # call parent init using bus I2C port
        super().__init__(I2C(SCL, SDA))
        # super().sea_level_pressure = self.SEA_LEVEL_PRESSURE


def handler(signal_received, frame):
    print("Measurement stopped by user.")

    exit(0)


if __name__ == "__main__":
    e = Environment()

    while True:
        print("\nTemperature: %0.1f C" % e.temperature)
        print("Humidity: %0.1f %%" % e.humidity)
        print("Pressure: %0.1f hPa" % e.pressure)
        print("Altitude = %0.2f meters" % e.altitude)
        sleep(1)

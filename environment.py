from board import SCL, SDA
from busio import I2C
from adafruit_bme280 import Adafruit_BME280_I2C


class Environment(Adafruit_BME280_I2C):
    SEA_LEVEL_PRESSURE = 1018.9

    def __init__(self):
        # call parent init using bus I2C port
        super().__init__(I2C(SCL, SDA))
        super().sea_level_pressure = self.SEA_LEVEL_PRESSURE


if __name__ == "__main__":
    e = Environment()
    print("\nTemperature: %0.1f C" % e.temperature)
    print("Humidity: %0.1f %%" % e.humidity)
    print("Pressure: %0.1f hPa" % e.pressure)
    print("Altitude = %0.2f meters" % e.altitude)

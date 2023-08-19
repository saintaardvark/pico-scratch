from machine import Pin, I2C
import utime
from mpu6050 import init_mpu6050, get_mpu6050_data

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
init_mpu6050(i2c)

while True:
    data = get_mpu6050_data(i2c)
    print("Temperature: {:.2f} °C".format(data["temp"]))
    print(
        "Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(
            data["accel"]["x"], data["accel"]["y"], data["accel"]["z"]
        )
    )
    print(
        "Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} °/s".format(
            data["gyro"]["x"], data["gyro"]["y"], data["gyro"]["z"]
        )
    )
    utime.sleep(0.5)

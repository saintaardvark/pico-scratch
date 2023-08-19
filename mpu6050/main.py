import utime
from mpu6050 import MPU6050

# i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

# Probably bogus values; this was done with the sensor at a random angle.
ofs = (878, -1385, 1560, 136, -54, -16)


def handler(data: tuple):
    if "mpu" in globals():
        print("[{:<16}] {:<10.2f}".format("TEMPERATURE", mpu.celsius))
        mpu.print_from_data(data)


class MyMpu(MPU6050):
    def start(self):
        """
        My own version of the Adafruit/eluke.nl code
        """
        # mpu->setMotionDetectionThreshold(1);
        self.__writeByte(0x1F, 0x01)
        # mpu->setMotionDetectionDuration(1);
        self.__writeByte(0x20, 0x01)
        # mpu->setInterruptPinLatch(true);	// Keep it latched.  Will turn off when reinitialized.
        # Want to set 5th (latch until clear).
        # Could *also* set 4th bit (clear by reading 0x3a / d58), but will leave that for now.
        self.__writeByte(0x37, 0x20)
        # mpu->setInterruptPinPolarity(true);
        # This is config'd by setting 0x37, 7th bit to 0.  Done above.
        # mpu->setMotionInterrupt(true);
        # IntEnable is 0x38.  Need to set 6th bit.
        self.__writeByte(0x38, 0x40)
        #
        # And finally, clear interrupts to get ready:
        self.reset_interrupt()

    def reset_interrupt(self):
        """
        This lets the next interrupt happen if interrupts are latched.
        """
        mpu.__readByte(0x3A)

if mpu.passed_self_test:
    print("Self-test passed, here we go!")
    mpu.start()

while True:
    print("Waiting...")
    utime.sleep(60)

    


mpu = MyMpu(0, 20, 21, ofs, 2, handler)

mpu = MyMpu(0, 20, 21, ofs, 2, handler)

# My own version of the Adafruit/eluke.nl code

# mpu->setMotionDetectionThreshold(1);
mpu.__writeByte(0x1F, 0x01)
# mpu->setMotionDetectionDuration(1);
mpu.__writeByte(0x20, 0x01)
# mpu->setInterruptPinLatch(true);	// Keep it latched.  Will turn off when reinitialized.
# Want to set 5th (latch until clear).
# Could *also* set 4th bit (clear by reading 0x3a / d58), but will leave that for now.
mpu.__writeByte(0x37, 0x20)
# mpu->setInterruptPinPolarity(true);
# This is config'd by setting 0x37, 7th bit to 0.  Done above.
# mpu->setMotionInterrupt(true);
# IntEnable is 0x38.  Need to set 6th bit.
mpu.__writeByte(0x38, 0x40)



# while True:
#     print(mp.data)
#     utime.sleep(1)

# data = get_mpu6050_data(i2c)
# print("Temperature: {:.2f} °C".format(data["temp"]))
# print(
#     "Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(
#         data["accel"]["x"], data["accel"]["y"], data["accel"]["z"]
#     )
# )
# print(
#     "Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} °/s".format(
#         data["gyro"]["x"], data["gyro"]["y"], data["gyro"]["z"]
#     )
# )
# utime.sleep(0.5)

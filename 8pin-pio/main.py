from machine import Pin
from time import sleep


MAX_PINS = 8  # offset by one because pins start at zero


def blink(outp, sleepytime=0.1):
    """Blink pin"""
    outp.on()
    sleep(sleepytime)
    outp.off()


def blink_and_check(outp, inp, sleepytime=0.1):
    """Blink pin and check input"""
    outp.on()
    val = inp.value()
    sleep(sleepytime)
    outp.off()
    return val


def main():
    """
    Main entry point
    """
    outputs = [Pin(i, Pin.OUT) for i in range(0, MAX_PINS)]
    inputs = [Pin(i + 8, Pin.IN) for i in range(0, MAX_PINS)]

    while True:
        vals = []
        for o, i in zip(outputs, inputs):
            vals.append(blink_and_check(o, i))

        print(vals)

        sleep(0.2)
        outputs.reverse()
        inputs.reverse()


if __name__ == "__main__":
    main()

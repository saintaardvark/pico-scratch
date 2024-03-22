from machine import Pin
from time import sleep


p = []
MAX_PINS = 8  # offset by one because pins start at zero

def blink(pin, sleepytime=0.1):
    """Blink pin"""
    pin.on()
    sleep(sleepytime)
    pin.off()
    

def main():
    """
    Main entry point
    """
    p = [Pin(i, Pin.OUT) for i in range(0, MAX_PINS)]

    while True:
        for i in p:
            blink(i)

        sleep(0.2)
        p.reverse()


if __name__ == "__main__":
    main()

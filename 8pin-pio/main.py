from machine import Pin
from time import sleep


p = []
MAX_PINS = 8  # offset by one because pins start at zero


def main():
    """
    Main entry point
    """
    p = [Pin(i, Pin.OUT) for i in range(0, MAX_PINS)]

    while True:
        for i in range(0, MAX_PINS):
            print(i)
            p[i].on()
            sleep(0.1)
            p[i].off()

        sleep(0.2)

        for i in range(MAX_PINS-1, -1, -1):
            print(i)
            p[i].on()
            sleep(0.1)
            p[i].off()

        sleep(0.2)


if __name__ == "__main__":
    main()

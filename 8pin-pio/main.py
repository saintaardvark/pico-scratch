from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

from paral import paral_prog, paral_read

MAX_PINS = 8  # offset by one because pins start at zero


def main():
    paral_sm = StateMachine(0, paral_prog, freq=2000, out_base=Pin(0))
    paral_read_sm = StateMachine(1, paral_read, freq=2000, in_base=Pin(8))
    paral_sm.active(1)
    paral_read_sm.active(1)

    while True:
        for i in range(500):
            paral_sm.put(i)
            print(f"i = {i}")
            r = paral_read_sm.get()
            print(f"Read: {r}")
            # We're reading in 8 bits; the TX buffer is 32 bits;
            # shift by 24.
            print(f"Shift: {r >> 24}")
            sleep(0.5)


if __name__ == "__main__":
    main()

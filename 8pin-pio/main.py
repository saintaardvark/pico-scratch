from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

from paral import clock, paral_read

MAX_PINS = 8  # offset by one because pins start at zero
JMP_PIN = Pin(8)


def main():
    read_sm = StateMachine(
        0, paral_read, freq=2000, in_base=Pin(0), sideset_base=JMP_PIN
    )
    clock_sm = StateMachine(1, clock, freq=2000, jmp_pin=JMP_PIN)
    # TODO: set both active at once
    read_sm.active(1)
    clock_sm.active(1)
    last = -1
    while True:
        r = paral_read_sm.get()
        r = r << 24
        if last == -1:
            last = r
        # print(f"Read: {r}")
        # We're reading in 8 bits; the TX buffer is 32 bits;
        # shift by 24.
        # print(f"Shift: {r >> 24}")
        if last != r:
            print(r)
        sleep(0.5)


if __name__ == "__main__":
    main()

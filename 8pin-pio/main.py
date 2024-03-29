from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

from paral import clock, paral_read

MAX_PINS = 8  # offset by one because pins start at zero
JMP_PIN = Pin(8)
# We're reading in 8 bits; the TX buffer is 32 bits;
RIGHT_SHIFT = 24

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
        r = read_sm.get()
        c = clock_sm.get()
        if last == -1:
            last = c
        print(f"Read: {r=}, {(last-c)=}, {bin(r >> RIGHT_SHIFT)=}")
        sleep(1.0)


if __name__ == "__main__":
    main()

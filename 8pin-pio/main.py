from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

MAX_PINS = 8  # offset by one because pins start at zero

@asm_pio(
    # https://docs.micropython.org/en/v1.17/library/rp2.html: if more
    # than one pin is used in the program, out_init() needs to be a
    # tuple.  That explains the requirement of a comma for this to
    # work; I presume that the single element in the tuple means "they
    # should all be like this".
    out_init=(PIO.OUT_HIGH,) * 8,
    out_shiftdir=PIO.SHIFT_RIGHT,
    autopull=True,
    pull_thresh=16,
)
def paral_prog():
    pull()
    out(pins, 8)


def main():
    paral_sm = StateMachine(0, paral_prog, freq=2000, out_base=Pin(0))
    paral_sm.active(1)

    while True:
        for i in range(500):
            paral_sm.put(i)
            print(i)
            sleep(0.5)


if __name__ == "__main__":
    main()

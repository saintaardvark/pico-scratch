from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

MAX_PINS = 8  # offset by one because pins start at zero

@asm_pio(set_init=PIO.OUT_LOW)
def pioblink():
    wrap_target()
    set(pins, 1) [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 0) [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    wrap()

@asm_pio(
    out_init=(PIO.OUT_HIGH,) * 8,
    out_shiftdir=PIO.SHIFT_RIGHT,
    autopull=True,
    pull_thresh=16,
)
def paral_prog():
    pull()
    out(pins, 8)


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
    paral_sm = StateMachine(0, paral_prog, freq=2000, out_base=Pin(0))
    paral_sm.active(1)

    while True:
        for i in range(500):
            paral_sm.put(i)
            print(i)
            sleep(0.5)


# def main():
#     """
#     Main entry point
#     """
#     outputs = [Pin(i, Pin.OUT) for i in range(0, MAX_PINS)]
#     inputs = [Pin(i + 8, Pin.IN) for i in range(0, MAX_PINS)]

#     while True:
#         vals = []
#         for o, i in zip(outputs, inputs):
#             vals.append(blink_and_check(o, i))

#         print(vals)

#         sleep(0.2)
#         outputs.reverse()
#         inputs.reverse()


if __name__ == "__main__":
    main()

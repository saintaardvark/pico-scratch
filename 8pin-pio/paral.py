from rp2 import PIO, StateMachine, asm_pio


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
def clock():
    set(x, 0)
    label("WAIT_FOR_P1_HIGH")
    # Wait for pin1 to be high
    jmp(pin, "PUSH")
    jmp(x_dec, "WAIT_FOR_P1_HIGH")
    label("PUSH")
    in(x, 32)
    push()
    jmp(x_dec, "WAIT_FOR_P1_HIGH")

@asm_pio(
    set_init=PIO.OUT_LOW, in_shiftdir=PIO.SHIFT_RIGHT, autopush=True, push_thresh=16
)
def paral_read():
    """
    Read in parallel
    """
    mov(y, pins)
    label("main_loop")
    mov(x, pins)
    jmp(x_not_y, "move_out").side(1)
    jmp("main_loop")
    label("move_out")
    in_(x, 8).side(0)
    push()
    mov(y, x)
    jmp("main_loop")

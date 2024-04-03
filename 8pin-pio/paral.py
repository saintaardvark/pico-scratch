from rp2 import PIO, StateMachine, asm_pio


@asm_pio(
    # https://docs.micropython.org/en/v1.17/library/rp2.html: if more
    # than one pin is used in the program, out_init() needs to be a
    # tuple.  That explains the requirement of a comma for this to
    # work; I presume that the single element in the tuple means "they
    # should all be like this".
    out_init=(PIO.OUT_HIGH,) * 8,
    out_shiftdir=PIO.SHIFT_RIGHT,
    autopush=True,
    push_thresh=32,
    fifo_join=PIO.JOIN_RX,  # This gives us 8 words in the RX buffer
)
def clock():
    set(x, 0)
    label("WAIT_FOR_P1_HIGH")
    # Wait for pin1 to be high
    jmp(pin, "PUSH")
    jmp(x_dec, "WAIT_FOR_P1_HIGH")
    label("PUSH")
    in_(x, 32)
    jmp(x_dec, "WAIT_FOR_P1_HIGH")


@asm_pio(
    set_init=PIO.OUT_LOW,
    in_shiftdir=PIO.SHIFT_RIGHT,
    sideset_init=PIO.OUT_LOW,
    autopush=True,
    push_thresh=8,
    fifo_join=PIO.JOIN_RX,  # This gives us 8 words in the RX buffer
)
def paral_read():
    """
    Read in parallel
    """
    mov(y, pins)
    label("main_loop")
    mov(x, pins)
    # The side set is the signal to the clock routine that we've just
    # seen a pin change.  The clock routine may take up to 3 cycles to
    # notice this, so we don't turn it off until we return from this
    # jump.
    jmp(x_not_y, "move_out").side(1)
    jmp("main_loop")
    label("move_out")
    in_(x, 8)
    push().side(0)
    mov(y, x)
    jmp("main_loop").side(0)

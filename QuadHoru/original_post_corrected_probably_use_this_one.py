# Source: https://forums.raspberrypi.com/viewtopic.php?t=306064&sid=f40cf17605a796b93c59b94721dd322b#p1842706
#
# This is a little bit different from main.py:
#
# - this post comes from the thread & the original author, whereas
#   main.py comes from J. Beale's github repo.
#
# - But also, this code was corrected by the original author (set vs
#   mov), and those changes don't seem to have been captured in the
#   github repo.
#
# - finally, the simulated signals are in here too.

from machine import Pin, mem32
from rp2 import asm_pio, StateMachine, PIO
from time import ticks_ms, ticks_diff
import array

# Simulation SM
@asm_pio(set_init=PIO.OUT_LOW)
def in_sig_sim():
    label("delay")
    jmp(x_dec, "delay")
    wrap_target()
    set(pins, 0)
    mov(y, isr)
    label("low")
    jmp(y_dec, "low")
    set(pins, 1)
    mov(y, isr)
    label("high")
    jmp(y_dec, "high")
    wrap()

@asm_pio(set_init=PIO.OUT_HIGH)
def trigger():
    # Wait for 1 (high) on pin 0.  For SM2, that's Pin 14.  For SM3,
    # that's Pin 15.
    wait(1, pin, 0)
    # Set pins to 1 (high) & do this for 2 add'l cycles.  For both state
    # machines, that's Pin 16.
    set(pins, 1) [2]
    # Set pins to 0 (low).  Again, Pin 16.
    set(pins, 0)
    # Wait for 0 (low) on pin 0.  For SM2, that's Pin 14.  For SM3,
    # that's Pin 15.
    wait(0, pin, 0)
    # Set pins to 1 (high) & do this for 2 add'l cycles.  For both state
    # machines, that's Pin 16.
    set(pins, 1) [2]
    # Set pins to 0.
    set(pins, 0)

@asm_pio(sideset_init=PIO.OUT_LOW)
def counter():
    # Set scratch register y to value 3
    set(y, 3)
    # wait for 1 (high) on pin 2.  This is the counter SM; its base
    # pin is 14, so we're waiting on pin 16 to show high.
    wait(1, pin, 2)
    # Wrap up here
    wrap_target()
    # Just a label
    label("loop")
    # Set scratch register x to value 0.  Simultaneously, set side pin
    # to 1 (high).  For the counter SM, that's pin 25 -- it's set in
    # the initialization of sm4 (sideset_base).
    set(x, 0) .side(1)
    # Wait for 0 (low) on pin 2.  Again, the base pin is 14, so we're
    # waiting on pin 16 to show low.
    wait(0, pin, 2)
    # Shift 2 bits from the pins we're watching to the Input Shift
    # Register.  This will be read later on by the interrupt handler.
    # We're reading 2 pins -- so starting at the base pin of 14, that
    # means reading the state of pins 14 & 15 & putting those in the
    # ISR.
    in_(pins, 2)
    # Push the contents of the ISR into the RX fifo as one 32-bit
    # word.  Set the ISR to all zeroes.
    push()
    # Jump to "counter start" if x is non-zero.  Irregardlessfully,
    # decrement x.
    jmp(x_dec, "counter_start")
    # Just a label
    label("counter_start")
    # Jmp to label output if pin is 1 (high).  The pin we check is set
    # by jmp_pin (EXECCTRL_JMP_PIN in assembly).  For SM4, that's pin
    # 16.
    jmp(pin, "output")
    # Jump to "counter start" if x is non-zero.  Irregardlessfully,
    # decrement x.
    jmp(x_dec, "counter_start")
    # Just a label.
    label("output")
    # Move the contents of scratch register x to the ISR -- *but*,
    # invert those bits first.  As a side effect, set side pin 25 to 0.
    mov(isr, invert(x)) .side(0)
    # Push the contents of the ISR into the RX fifo as one 32-bit
    # word.  Set the ISR to all zeroes.
    push()
    # Jump to "loop" if y is non-zero.  Irregardlessfully,
    # decrement y.
    jmp(y_dec, "loop")
    # Set IRQ 0x10 and wait for it to be cleared before proceeding.
    irq(block, 0x10)
    # Set scratch register y to value 3.  As a side effet, set side
    # pin 25 to 0.
    set(y, 3) .side(0)
    # Wrap back to wrap target.
    wrap()

data = array.array("I", [0]*8)
start = ticks_ms()
def counter_handler(sm):
    global start
    for i in range(8):
        data[i] = sm.get()
    print(ticks_diff(ticks_ms(), start), data)
    start = ticks_ms()

# Instantiate and configure signal simulating SMs
sm0 = StateMachine(0, in_sig_sim, freq=1_000_000, set_base=Pin(14))
sm0.put(500_000) # Frequency control
sm0.exec("pull()")
sm0.exec("mov(isr, osr)")
sm0.put(100_000) # Delay control
sm0.exec("pull()")
sm0.exec("mov(x, osr)")
sm1 = StateMachine(1, in_sig_sim, freq=1_000_000, set_base=Pin(15))
sm1.put(500_000) # Frequency control
sm1.exec("pull()")
sm1.exec("mov(isr, osr)")
sm1.put(1) # Delay control
sm1.exec("pull()")
sm1.exec("mov(x, osr)")

sm2 = StateMachine(2, trigger, freq=100_000_000, in_base=Pin(14), set_base = Pin(16))
sm2.active(1)
sm3 = StateMachine(3, trigger, freq=100_000_000, in_base=Pin(15), set_base = Pin(16))
sm3.active(1)

sm4 = StateMachine(4, counter, freq=100_000_000, in_base=Pin(14), jmp_pin = Pin(16), sideset_base=Pin(25))
sm4.irq(counter_handler)

PIO0_BASE = 0x50200000
PIO1_BASE = 0x50300000
PIO_CTRL =  0x000
SM0_EXECCTRL = 0x0cc
SM0_SHIFTCTRL = 0x0d0
# Join output FIFOs for sm4
mem32[PIO1_BASE | SM0_SHIFTCTRL + 0x1000] = 1<<31
sm4.active(1)
# Start sm0 and sm1 in sync
mem32[PIO0_BASE | PIO_CTRL + 0x1000] = 0b11

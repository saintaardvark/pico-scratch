# https://forums.raspberrypi.com/viewtopic.php?t=306064&sid=01111b75f3f4864611b944ba26c707d3de
# PIO measure period of 1-PPS input signal on Pin 16, based on
# https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/pio_pinchange.py

import time
from machine import Pin
import rp2
# -----------------------------------------------------

@rp2.asm_pio()
def wait_pin_low():
    wrap_target()
    wait(0, pin, 0)
    irq(block, rel(0))
    wait(1, pin, 0)
    wrap()

def handler(sm):   # interrupt handler for detected edge
  global timestamp
  global flagNew
  timestamp = time.ticks_us()
  flagNew = True

# ----- Main program starts here -------------------

pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
sm0 = rp2.StateMachine(0, wait_pin_low, in_base=pin16)
sm0.irq(handler)

global flagNew
flagNew = False
oldStamp = 0

sm0.active(1)  # start the PIO state machine running

pulseCount = 0 # how many pulses we have received
dMax = -99999  # initialize to opposite extremes
dMin = 99999
# delta interval between pulses should ideally be 1000000 us
while True:
    if flagNew:
        delta = (timestamp - oldStamp) - 1000000
        oldStamp = timestamp
        flagNew = False
        pulseCount += 1
        if pulseCount > 3:
          if (delta > dMax):
              dMax = delta
          if (delta < dMin):
              dMin = delta

        if (pulseCount % 100) == 0:
          print(pulseCount,dMin,dMax)

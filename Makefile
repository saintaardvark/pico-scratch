# https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython
FIRMWARE=micropython-firmware-pico-w-130623.uf2
URL=https://datasheets.raspberrypi.com/soft/$(FIRMWARE)
DEV?=/dev/ttyACM0
RSHELL=rshell --port $(DEV)
MODEM_SPEED=115200

install_micropython: data/$(FIRMWARE)


.PHONY: install_boot
install_boot: kill_console
	$(RSHELL) cp boot.py /pyboard/

install_%: kill_console
	$(RSHELL) rsync $*/ /pyboard/

.PHONY: repl
repl:
	$(RSHELL) repl

.PHONY: rshell
rshell:
	$(RSHELL)

console: terminal
terminal:
	~/bin/espconsole.sh
	# screen $(DEV) $(MODEM_SPEED)

.PHONY: kill_console
kill_console:
	@-pkill -9 screen

data/$(FIRMWARE):
	cd data && wget $(URL)

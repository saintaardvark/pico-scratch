# https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython
FIRMWARE=micropython-firmware-pico-w-130623.uf2
URL=https://datasheets.raspberrypi.com/soft/$(FIRMWARE)

install_micropython: data/$(FIRMWARE)


data/$(FIRMWARE):
	cd data && wget $(URL)

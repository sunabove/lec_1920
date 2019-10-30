# coding: utf-8
from gpiozero import LED
from time import sleep

led = LED(26)

print( "Press Ctrl + C to quit! ")

while True:
	led.on()
	print("+", end = '', flush=True )
	sleep(1)
	led.off()
	print("\b-", end = '', flush=True)
	sleep(1)
	print("\b", end = '', flush=True)
pass


# coding: utf-8
#!/usr/bin/env python 
import time
import sys
import signal

def signal_handler(signal, frame):
   # ctrl + c -> exit program

   print('You pressed Ctrl+C!')

   gpio.cleanup()

   sys.exit(0)
pass

signal.signal(signal.SIGINT, signal_handler)


print ('---------- sonar start ----------') 

# coding: utf-8
from time import sleep
import RPi.GPIO as gpio
# Use "GPIO" pin numbering
gpio.setmode(gpio.BCM)
# Set LED pin as output
pin_no = 4
gpio.setup(pin_no, gpio.IN, pull_up_down=gpio.PUD_UP) 
sleep(1)

while 1 : 
   v = gpio.input( pin_no )
   print( v , end="" )
   #sleep( 0.018/10 )
pass

gpio.cleanup()

print( "----------- Good bye! ---------")
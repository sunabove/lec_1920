# coding: utf-8
#!/usr/bin/env python 
import time
import sys
import signal

def signal_handler(signal, frame):
   # ctrl + c -> exit program

   print('You pressed Ctrl+C!')
   sys.exit(0)
pass

signal.signal(signal.SIGINT, signal_handler)


print ('---------- sonar start ----------') 

#!/usr/bin/env python


import time
import serial

ser = serial.Serial(   
   port='/dev/ttyAMA0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
) 

idx = 0 

while ser.is_open :
   c = ser.read( 1 )
   print( c.hex() , end="" )
   idx += 1
pass

print( "----------- Good bye! ---------")
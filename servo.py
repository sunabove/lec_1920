# coding: utf-8
from gpiozero import Servo
from time import sleep

servo = Servo(4) 

for i in range( 0 ) :
   print( "servo min")
   servo.min()
   sleep(1)
   print( "servo mid")
   servo.mid()
   sleep(1)
   print( "servo max")
   servo.max()
   sleep(1)
   print( "servo value 0.5")
   servo.value = 0.5
   sleep(1)
pass

for i in range( -10, 10 ) :   
   servo.value = i/10.0
   print( "servo value = %5.4f" % servo.value )
   sleep(1)
pass

if 1 :
   print( "servo mid")
   servo.mid()
   sleep(1)
pass

if 0 :   
   servo.value = -0.9
   print( "servo value = %5.4f" % servo.value )
   sleep(2)
pass

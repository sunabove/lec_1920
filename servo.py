# coding: utf-8
from gpiozero import Servo
from time import sleep

servo = Servo(4)

for i in range( 1 ) :
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

print( "servo mid")
servo.mid()
sleep(1)
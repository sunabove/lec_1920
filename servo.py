# coding: utf-8
from gpiozero import Servo
from time import sleep

servo = Servo(4)

while True:
   print( "servo min")
   servo.min()
   sleep(5)
   print( "servo mid")
   servo.mid()
   sleep(5)
   print( "servo max")
   servo.max()
   sleep(5)
   print( "servo value 0.5")
   servo.value = 0.5
   sleep(5)
pass

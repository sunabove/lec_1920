# coding: utf-8
from gpiozero import Motor
from time import sleep

motor = Motor(forward=22, back=23)

while 1 :
   motor.forward()
   sleep(5)
   motor.backward()
   sleep(5)
pass

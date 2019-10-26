# coding: utf-8
from gpiozero import Motor
from time import sleep

motor = Motor(forward=4, backward=14)

motor.forward()
sleep(3)
motor.backward()
sleep(3)

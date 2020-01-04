# coding: utf-8

from gpiozero import PWMLED
from time import sleep

pwmESC = PWMLED(17)

value_min = 0.148
value_max = 0.151
value_gap = value_max - value_min

steps = 20
for x in range( steps ) :
   pwmESC.value = value_min + value_gap*x/(steps + 0.0)
   print( "pwm value = %5.4f" % pwmESC.value )
   sleep(0.7) 
pass

pwmESC.value = 0

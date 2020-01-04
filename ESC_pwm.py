# coding: utf-8

from gpiozero import PWMLED
from time import sleep

esc = PWMLED(17)

value_min = 0.146 
value_max = 0.152
value_gap = value_max - value_min

steps = 20
for x in range( steps ) :
   esc.value = value_min + value_gap*x/(steps + 0.0)
   print( "pwm value = %5.4f" % esc.value )
   sleep(0.7) 
pass

esc.value = 0

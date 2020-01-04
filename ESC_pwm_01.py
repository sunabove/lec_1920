# coding: utf-8

from gpiozero import PWMLED
from time import sleep 

esc = PWMLED(17)

esc.value = 0
sleep( 0.7)

for x in range( 10, 50 ):
    esc.value = x*0.01
    print( "pwm value = %5.2f" % esc.value )
    sleep( 0.7 ) 
pass

esc.value = 0


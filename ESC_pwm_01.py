# coding: utf-8

from gpiozero import PWMLED
from time import sleep 
from numpy import arange

esc = PWMLED(17)

esc.value = 0
sleep( 1 )

for x in arange( 0.145, 0.157, 0.001 ):
    esc.value = x
    print( "pwm value = %5.4f" % esc.value )
    sleep( 1 ) 
pass

esc.value = 0


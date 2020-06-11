# coding: utf-8
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=17, trigger=4)
while 1 :
   print( 'Distance: ', 100*sensor.distance, 'cm' )
   sleep( 0.018 )
pass

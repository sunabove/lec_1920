# coding: utf-8
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=15, trigger=14)
prev_dist = 0 
while 1 :
   dist = 100*sensor.distance
   if abs( dist - prev_dist ) > 0.001 :
      print( 'Distance: ', dist , 'cm' )
      prev_dist = dist
   pass
   sleep( 0.018 )
pass

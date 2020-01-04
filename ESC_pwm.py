# coding: utf-8

import os 
import time 
#Launching GPIO library
os.system ("sudo pigpiod") 
time.sleep(1) 
import pigpio  

esc_gpio = 17  #Connect the ESC in this GPIO pin 

pi = pigpio.pi()
pi.set_servo_pulsewidth(esc_gpio, 0) 

time.sleep(3) 

min_value = 1520 
max_value = 1600   

speed = min_value

while speed < max_value :  
   print( "speed = %d" % speed )
   pi.set_servo_pulsewidth( esc_gpio, speed)
   time.sleep( 1 )
   speed += 10
pass 

pi.set_servo_pulsewidth(esc_gpio, 0) 
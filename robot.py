# coding: utf-8
from gpiozero import Robot
from time import sleep

#robot = Robot(left=(4, 14), right=(17, 18))
robot = Robot(left=(22, 23), right=(9, 25))

interval = 2
print( "Moving forward ..." )
robot.forward()
sleep(interval)
print( "Moving left ..." )
robot.left()
sleep(interval)
print( "Moving right ..." )
robot.right()
sleep(interval)
print( "Moving backward ..." )
robot.backward()
sleep(interval)

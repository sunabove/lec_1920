from gpiozero import Robot
from time import sleep

robot = Robot(left=(4, 14), right=(17, 18))

interval = 2
robot.forward()
sleep(interval)
robot.left()
sleep(interval)
robot.right()
sleep(interval)
robot.backward()
sleep(interval)

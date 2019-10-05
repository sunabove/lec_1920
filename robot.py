from gpiozero import Robot
from time import sleep

robot = Robot(left=(4, 14), right=(17, 18))

for i in range(4):
    robot.forward()
    sleep(1)
    robot.backward()
    robot.revers()
    sleep(1)
pass
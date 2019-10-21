# coding: utf-8
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.brightness = 70
camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/bright.jpg')
camera.stop_preview()
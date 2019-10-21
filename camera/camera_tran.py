# coding: utf-8
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview(alpha=200)
sleep(60)
camera.stop_preview()
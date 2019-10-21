# coding: utf-8

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.start_recording( '/home/pi/Desktop/effects.h264' )
sleep(3) 
idx = 0 
for effect in camera.IMAGE_EFFECTS:
    camera.image_effect = effect
    camera.annotate_text = "%02d : %s" % (idx + 1, effect)
    sleep(3)
    idx += 1
camera.stop_recording()
camera.stop_preview()
# coding: utf-8
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

t1 = GPIO.PWM(11, 60)

t1.start(0)

#t1.ChangeDutyCycle(7.5)
time.sleep(3)

t1.stop()

GPIO.cleanup()
quit()
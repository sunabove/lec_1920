# coding: utf-8
#
# Sends the servo pulses needed to initialise some ESCs
#
# Requires the pigpio daemon to be running
#
# sudo apt install pigpiod
# sudo pigpiod

import time

import pigpio

SERVO = 4

pi = pigpio.pi() # Connect to local Pi.

pi.set_servo_pulsewidth(SERVO, 1000) # Minimum throttle.

time.sleep(5)

pi.set_servo_pulsewidth(SERVO, 2000) # Maximum throttle.

time.sleep(5)

pi.set_servo_pulsewidth(SERVO, 1100) # Slightly open throttle.

time.sleep(5)

pi.set_servo_pulsewidth(SERVO, 0) # Stop servo pulses.

pi.stop() # Disconnect from local Raspberry Pi.
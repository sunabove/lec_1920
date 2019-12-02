#!/usr/bin/python
#   This program is used to calibrate the compass on a BerryIMUv1 or
#   BerryIMUv2.
#
#   Start this program and rotate your BerryIMU in all directions. 
#   You will see the maximum and minimum values change. 
#   After about 30secs or when the values are not changing, press Ctrl-C.
#   The program will printout some text which you then need to add to
#   berryIMU.py or berryIMU-simple.py


import sys,signal,os
import time
import math

import IMU
import datetime


def handle_ctrl_c(signal, frame):
    print( " " )
    print( "magXmin = ",  magXmin )
    print( "magYmin = ",  magYmin )
    print( "magZmin = ",  magZmin )
    print( "magXmax = ",  magXmax )
    print( "magYmax = ",  magYmax )
    print( "magZmax = ",  magZmax )
    sys.exit(130) # 130 is standard exit code for ctrl-c



IMU.detectIMU()
IMU.initIMU()

#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)


#Preload the variables used to keep track of the minimum and maximum values
magXmin = 32767
magYmin = 32767
magZmin = 32767
magXmax = -32767
magYmax = -32767
magZmax = -32767


def calibrate_imu( ) : 
    global magXmin 
    global magYmin 
    global magZmin 
    global magXmax 
    global magYmax 
    global magZmax 

    start = time.perf_counter()

    cnt = 0 
    while time.perf_counter() - start < 10 : 

        cnt += 1

        #Read magnetometer values
        MAGx = IMU.readMAGx()
        MAGy = IMU.readMAGy()
        MAGz = IMU.readMAGz() 
        
        
        if MAGx > magXmax:
            magXmax = MAGx
        if MAGy > magYmax:
            magYmax = MAGy
        if MAGz > magZmax:
            magZmax = MAGz

        if MAGx < magXmin:
            magXmin = MAGx
        if MAGy < magYmin:
            magYmin = MAGy
        if MAGz < magZmin:
            magZmin = MAGz

        format = "IMU Cali [%06d] magXmin  %i  magYmin  %i  magZmin  %i  ## magXmax  %i  magYmax  %i  magZmax %i"
        print( format %(cnt, magXmin,magYmin,magZmin,magXmax,magYmax,magZmax) , end = "" )
        
        #slow program down a bit, makes the output more readable
        time.sleep(0.03)
        print( "\b"*200)
    pass
pass

if __name__ == '__main__':
    calibrate_imu( )
pass

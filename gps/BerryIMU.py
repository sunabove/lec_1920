# coding: utf-8 

import sys
import time
import math
import IMU
import datetime
import os
# If the IMU is upside down (Skull logo facing up), change this value to 1
IMU_UPSIDE_DOWN = 0	


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      	# Complementary filter constant
MAG_LPF_FACTOR = 0.4 	# Low pass filter constant magnetometer
ACC_LPF_FACTOR = 0.4 	# Low pass filter constant for accelerometer
ACC_MEDIANTABLESIZE = 9    	# Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 9    	# Median filter table size for magnetometer. Higher = smoother but a longer delay



################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values 
# Calibrating the compass isnt mandatory, however a calibrated 
# compass will result in a more accurate heading value.

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0


'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''



#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0

class ImuData :
    def __init__( self ) :
        self.dbg = 0 

        self.imu_cnt = 0 

        self.gyroXangle = 0.0
        self.gyroYangle = 0.0
        self.gyroZangle = 0.0

        self.heading = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0

        self.pitch_deg = 0.0
        self.roll_deg = 0.0
        self.yaw_deg = 0.0

        self.kalmanX = 0.0
        self.kalmanY = 0.0
        pass
    pass
pass

class BerryIMU : 
    def __init__( self ) :
        self.dbg = 0
        self.init_curses = 0 
        self.use_curses = 0 
        self.imu_cnt = 0 
        self.imuData = ImuData()
        self.imuData.dbg = self.dbg
        self.calibrated = 0 
        pass
    pass

    def __del__(self):
        if self.use_curses and self.init_curses :
            import curses
            curses.endwin() 
        pass
    pass

    def kalmanFilterY ( self, accAngle, gyroRate, DT):
        y=0.0
        S=0.0

        global KFangleY
        global Q_angle
        global Q_gyro
        global y_bias
        global YP_00
        global YP_01
        global YP_10
        global YP_11

        KFangleY = KFangleY + DT * (gyroRate - y_bias)

        YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
        YP_01 = YP_01 + ( - DT * YP_11 )
        YP_10 = YP_10 + ( - DT * YP_11 )
        YP_11 = YP_11 + ( + Q_gyro * DT )

        y = accAngle - KFangleY
        S = YP_00 + R_angle
        K_0 = YP_00 / S
        K_1 = YP_10 / S
        
        KFangleY = KFangleY + ( K_0 * y )
        y_bias = y_bias + ( K_1 * y )
        
        YP_00 = YP_00 - ( K_0 * YP_00 )
        YP_01 = YP_01 - ( K_0 * YP_01 )
        YP_10 = YP_10 - ( K_1 * YP_00 )
        YP_11 = YP_11 - ( K_1 * YP_01 )
        
        return KFangleY

    def kalmanFilterX (self, accAngle, gyroRate, DT):
        x=0.0
        S=0.0

        global KFangleX
        global Q_angle
        global Q_gyro
        global x_bias
        global XP_00
        global XP_01
        global XP_10
        global XP_11


        KFangleX = KFangleX + DT * (gyroRate - x_bias)

        XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
        XP_01 = XP_01 + ( - DT * XP_11 )
        XP_10 = XP_10 + ( - DT * XP_11 )
        XP_11 = XP_11 + ( + Q_gyro * DT )

        x = accAngle - KFangleX
        S = XP_00 + R_angle
        K_0 = XP_00 / S
        K_1 = XP_10 / S
        
        KFangleX = KFangleX + ( K_0 * x )
        x_bias = x_bias + ( K_1 * x )
        
        XP_00 = XP_00 - ( K_0 * XP_00 )
        XP_01 = XP_01 - ( K_0 * XP_01 )
        XP_10 = XP_10 - ( K_1 * XP_00 )
        XP_11 = XP_11 - ( K_1 * XP_01 )
        
        return KFangleX
    pass


    def read_imu_thread(self) :
        from threading import Thread
        Thread( target=self.read_imu ).start() 
    pass

    def calibrate_imu( self ) : 
        if 1 == self.calibrated : # 캘리브레이션 중이면 중복으로 캘리하지 않는다.
            return
        pass

        self.calibrated = 1 

        IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
        IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass 

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

            print( "\b"*100)
            
            #slow program down a bit, makes the output more readable
            time.sleep(0.03)            

            format = "IMU Cali [%06d] Mag Xmin  %i  Ymin  %i  Zmin  %i  ## Xmax  %i  Ymax  %i  Zmax %i"
            print( format %(cnt, magXmin,magYmin,magZmin,magXmax,magYmax,magZmax) , end = "" ) 
            
        pass

        print( "\nIMU calibration has completed.")
    pass

    def read_imu( self ) : 
        dbg = self.dbg

        IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
        IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

        # calibrate IMU
        if not self.calibrated : 
            self.calibrate_imu()

            self.calibrated = 2
        pass

        gyroXangle = 0.0
        gyroYangle = 0.0
        gyroZangle = 0.0

        CFangleX = 0.0
        CFangleY = 0.0
        CFangleXFiltered = 0.0
        CFangleYFiltered = 0.0
        
        kalmanX = 0.0
        kalmanY = 0.0
        
        oldXMagRawValue = 0
        oldYMagRawValue = 0
        oldZMagRawValue = 0
        oldXAccRawValue = 0
        oldYAccRawValue = 0
        oldZAccRawValue = 0

        #Setup the tables for the mdeian filter. Fill them all with '1' so we dont get devide by zero error 
        acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
        acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
        acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
        acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
        acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
        acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE
        mag_medianTable1X = [1] * MAG_MEDIANTABLESIZE
        mag_medianTable1Y = [1] * MAG_MEDIANTABLESIZE
        mag_medianTable1Z = [1] * MAG_MEDIANTABLESIZE
        mag_medianTable2X = [1] * MAG_MEDIANTABLESIZE
        mag_medianTable2Y = [1] * MAG_MEDIANTABLESIZE
        mag_medianTable2Z = [1] * MAG_MEDIANTABLESIZE

        a = datetime.datetime.now()

        processing = 0 
        while 1 :
            if not processing : 
                processing = 1 

                self.imu_cnt += 1

                #Read the accelerometer,gyroscope and magnetometer values
                ACCx = IMU.readACCx()
                ACCy = IMU.readACCy()
                ACCz = IMU.readACCz()
                GYRx = IMU.readGYRx()
                GYRy = IMU.readGYRy()
                GYRz = IMU.readGYRz()
                MAGx = IMU.readMAGx()
                MAGy = IMU.readMAGy()
                MAGz = IMU.readMAGz()


                #Apply compass calibration    
                MAGx -= (magXmin + magXmax) /2 
                MAGy -= (magYmin + magYmax) /2 
                MAGz -= (magZmin + magZmax) /2 
            

                ##Calculate loop Period(LP). How long between Gyro Reads
                b = datetime.datetime.now() - a
                a = datetime.datetime.now()
                LP = b.microseconds/(1000000*1.0)

                ############################################### 
                #### Apply low pass filter ####
                ###############################################
                MAGx =  MAGx  * MAG_LPF_FACTOR + oldXMagRawValue*(1 - MAG_LPF_FACTOR)
                MAGy =  MAGy  * MAG_LPF_FACTOR + oldYMagRawValue*(1 - MAG_LPF_FACTOR)
                MAGz =  MAGz  * MAG_LPF_FACTOR + oldZMagRawValue*(1 - MAG_LPF_FACTOR)
                ACCx =  ACCx  * ACC_LPF_FACTOR + oldXAccRawValue*(1 - ACC_LPF_FACTOR)
                ACCy =  ACCy  * ACC_LPF_FACTOR + oldYAccRawValue*(1 - ACC_LPF_FACTOR)
                ACCz =  ACCz  * ACC_LPF_FACTOR + oldZAccRawValue*(1 - ACC_LPF_FACTOR)

                oldXMagRawValue = MAGx
                oldYMagRawValue = MAGy
                oldZMagRawValue = MAGz
                oldXAccRawValue = ACCx
                oldYAccRawValue = ACCy
                oldZAccRawValue = ACCz

                ######################################### 
                #### Median filter for accelerometer ####
                #########################################
                # cycle the table
                for x in range (ACC_MEDIANTABLESIZE-1,0,-1 ):
                    acc_medianTable1X[x] = acc_medianTable1X[x-1]
                    acc_medianTable1Y[x] = acc_medianTable1Y[x-1]
                    acc_medianTable1Z[x] = acc_medianTable1Z[x-1]

                # Insert the lates values
                acc_medianTable1X[0] = ACCx
                acc_medianTable1Y[0] = ACCy
                acc_medianTable1Z[0] = ACCz    

                # Copy the tables
                acc_medianTable2X = acc_medianTable1X[:]
                acc_medianTable2Y = acc_medianTable1Y[:]
                acc_medianTable2Z = acc_medianTable1Z[:]

                # Sort table 2
                acc_medianTable2X.sort()
                acc_medianTable2Y.sort()
                acc_medianTable2Z.sort()

                # The middle value is the value we are interested in
                ACCx = acc_medianTable2X[int( ACC_MEDIANTABLESIZE/2 )]
                ACCy = acc_medianTable2Y[int( ACC_MEDIANTABLESIZE/2 )]
                ACCz = acc_medianTable2Z[int( ACC_MEDIANTABLESIZE/2 )]



                ######################################### 
                #### Median filter for magnetometer ####
                #########################################
                # cycle the table
                for x in range (MAG_MEDIANTABLESIZE-1,0,-1 ):
                    mag_medianTable1X[x] = mag_medianTable1X[x-1]
                    mag_medianTable1Y[x] = mag_medianTable1Y[x-1]
                    mag_medianTable1Z[x] = mag_medianTable1Z[x-1]

                # Insert the latest values    
                mag_medianTable1X[0] = MAGx
                mag_medianTable1Y[0] = MAGy
                mag_medianTable1Z[0] = MAGz    

                # Copy the tables
                mag_medianTable2X = mag_medianTable1X[:]
                mag_medianTable2Y = mag_medianTable1Y[:]
                mag_medianTable2Z = mag_medianTable1Z[:]

                # Sort table 2
                mag_medianTable2X.sort()
                mag_medianTable2Y.sort()
                mag_medianTable2Z.sort()

                # The middle value is the value we are interested in
                MAGx = mag_medianTable2X[int( MAG_MEDIANTABLESIZE/2 )]
                MAGy = mag_medianTable2Y[int( MAG_MEDIANTABLESIZE/2 )]
                MAGz = mag_medianTable2Z[int( MAG_MEDIANTABLESIZE/2 )]



                #Convert Gyro raw to degrees per second
                rate_gyr_x =  GYRx * G_GAIN
                rate_gyr_y =  GYRy * G_GAIN
                rate_gyr_z =  GYRz * G_GAIN


                #Calculate the angles from the gyro. 
                gyroXangle+=rate_gyr_x*LP
                gyroYangle+=rate_gyr_y*LP
                gyroZangle+=rate_gyr_z*LP

                #Convert Accelerometer values to degrees

                if not IMU_UPSIDE_DOWN:
                    # If the IMU is up the correct way (Skull logo facing down), use these calculations
                    AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
                    AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
                else:
                    #Us these four lines when the IMU is upside down. Skull logo is facing up
                    AccXangle =  (math.atan2(-ACCy,-ACCz)*RAD_TO_DEG)
                    AccYangle =  (math.atan2(-ACCz,-ACCx)+M_PI)*RAD_TO_DEG



                #Change the rotation value of the accelerometer to -/+ 180 and
                #move the Y axis '0' point to up.  This makes it easier to read.
                if AccYangle > 90:
                    AccYangle -= 270.0
                else:
                    AccYangle += 90.0
                pass



                #Complementary filter used to combine the accelerometer and gyro values.
                CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
                CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle

                #Kalman filter used to combine the accelerometer and gyro values.
                kalmanY = self.kalmanFilterY(AccYangle, rate_gyr_y,LP)
                kalmanX = self.kalmanFilterX(AccXangle, rate_gyr_x,LP)

                if IMU_UPSIDE_DOWN:
                    MAGy = -MAGy      #If IMU is upside down, this is needed to get correct heading.
                pass

                #Calculate heading
                heading = 180 * math.atan2(MAGy,MAGx)/M_PI

                #Only have our heading between 0 and 360
                if heading < 0:
                    heading += 360
                pass



                ####################################################################
                ###################Tilt compensated heading#########################
                ####################################################################
                #Normalize accelerometer raw values.
                if not IMU_UPSIDE_DOWN:        
                    #Use these two lines when the IMU is up the right way. Skull logo is facing down
                    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
                    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
                else:
                    #Us these four lines when the IMU is upside down. Skull logo is facing up
                    accXnorm = -ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
                    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

                #Calculate pitch and roll

                pitch = math.asin(accXnorm)
                roll = -math.asin(accYnorm/math.cos(pitch))


                #Calculate the new tilt compensated values
                magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
            
                #The compass and accelerometer are orientated differently on the LSM9DS0 and LSM9DS1 and the Z axis on the compass
                #is also reversed. This needs to be taken into consideration when performing the calculations
                if(IMU.LSM9DS0):
                    magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS0
                else:
                    magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS1
                pass




                #Calculate tilt compensated heading
                tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

                if tiltCompensatedHeading < 0:
                    tiltCompensatedHeading += 360
                pass

                ############################ END ##################################

                imuData = ImuData() 

                imuData.imu_cnt = self.imu_cnt 

                imuData.gyroXangle = gyroXangle
                imuData.gyroYangle = gyroYangle
                imuData.gyroZangle = gyroZangle

                imuData.heading = heading
                imuData.roll = roll
                imuData.pitch = pitch
                imuData.yaw = math.radians(heading)

                imuData.roll_deg = math.degrees(roll)
                imuData.pitch_deg = math.degrees(pitch)
                imuData.yaw_deg = heading

                imuData.kalmanX = kalmanX
                imuData.kalmanY = kalmanY

                self.imuData = imuData  

                if not self.dbg :
                    pass
                elif self.use_curses :
                    import curses

                    if not self.init_curses : 
                        self.init_curses = 1
                        screen = curses.initscr()
                    pass

                    # Update the buffer, adding text at different locations
                    
                    sx = 0
                    sy = 0
                    screen.addstr(sy, sx, "Loop Time | %5.2f|" % ( LP ) )
                    sy += 1
                    screen.addstr(sy, sx, "# ACCX Angle %5.2f ACCY Angle %5.2f #  " % (AccXangle, AccYangle)) 
                    sy += 1
                    screen.addstr(sy, sx, "# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)) 
                    sy += 1
                    screen.addstr(sy, sx, "# CFangleX Angle %5.2f   CFangleY Angle %5.2f #" % (CFangleX,CFangleY)) 
                    sy += 1
                    screen.addstr(sy, sx, "# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)) 
                    sy += 1
                    screen.addstr(sy, sx, "# kalmanX %5.2f   kalmanY %5.2f #" % (kalmanX,kalmanY)) 
                    sy += 1
                    screen.addstr(sy, sx, "" ) 

                    # Changes go in to the screen buffer and only get
                    # displayed after calling `refresh()` to update
                    screen.refresh()
                    curses.napms(2000)
                else : 
                    if dbg : 
                        print( "Loop Time | %5.2f|" % ( LP ) )
                    pass  
                
                    if dbg :			#Change to '0' to stop showing the angles from the accelerometer
                        print ("# ACCX Angle %5.2f ACCY Angle %5.2f #  " % (AccXangle, AccYangle)),

                    if dbg :			#Change to '0' to stop  showing the angles from the gyro
                        print ("# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)),

                    if dbg:			#Change to '0' to stop  showing the angles from the complementary filter
                        print ("# CFangleX Angle %5.2f   CFangleY Angle %5.2f #" % (CFangleX,CFangleY)),
                        
                    if dbg:			#Change to '0' to stop  showing the heading
                        print ("# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)),
                        
                    if dbg:			#Change to '0' to stop  showing the angles from the Kalman filter
                        print ("# kalmanX %5.2f   kalmanY %5.2f #" % (kalmanX,kalmanY)),

                    #print a new line
                    print( ""   )
                pass

                processing = 0 

                #slow program down a bit, makes the output more readable
                time.sleep(0.01)
            pass
            
        pass

    pass
pass

if __name__ == '__main__':
    berryIMU = BerryIMU()
    berryIMU.use_curses = 0
    berryIMU.dbg = 1
    
    try : 
        berryIMU.read_imu()
    except Exception as e:
        print( e )
    pass
pass
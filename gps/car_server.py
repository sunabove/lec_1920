# coding: utf-8

def check_pkg( pkg ) : 
	try:
		import importlib
		mode_name = pkg.split(",")[0].strip() 
		importlib.import_module( mode_name )
	except ModuleNotFoundError :
		print( '%s is not installed, installing it now!' % mode_name )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg.split(",")[-1].strip() ] )
	pass
pass

for pkg in [ "flask", "OpenSSL, pyopenssl", "serial, pyserial", "pynmea2" ] :
	check_pkg( pkg )
pass

# default import packages
import time
from time import sleep
import threading
import math

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
# -- default import packages

# gps

import serial
import pynmea2

class Gps : 
    def __init__(self):
        self.gps_parse_cnt = 0
        self.lat = 0
        self.lon = 0
        self.alt = 0 
        self.msg = None
        self.dbg = 0
        self.gps_cnt = 0 
    pass

    def parseGPS(self, str):
        if 'GGA' in str :
            self.gps_parse_cnt += 1
            gps_parse_cnt = self.gps_parse_cnt
            msg = pynmea2.parse(str)
            msg.gps_parse_cnt = gps_parse_cnt 

            self.msg = msg 

            if self.dbg : 
                print( "[%04d] %s" % ( gps_parse_cnt, str ) , end ="" )
                format = "[%04d] Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" 
                print( format % ( gps_parse_cnt, msg.timestamp, msg.lat,msg.lat_dir, msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats) )
            pass
        pass
    pass 

    def read_gps_thread(self) :
        from threading import Thread
        Thread( target=self.read_gps_impl ).start() 
    pass

    def read_gps_impl(self) :
        while 1 :  
            try : 
                gps_serial = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 20 )
                while gps_serial :
                    str = gps_serial.readline()
                    self.parseGPS(str.decode( "utf-8"))
                    self.gps_cnt += 1
                pass
            except Exception as e:
                if self.dbg : 
                    print( str(e) )
                #print( "Serial Device Error" )
                #import time
                #time.sleep( 1 )
                pass
            pass
        pass
    pass 
pass

# -- gps

# car

class State :
    FORWARD = "FORWARD"
    BACKWARD = "BACKEARD"
    STOP = "STOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT" 
    REVERSE = "REVERSE"
pass
    
from gpiozero import Robot, LED

class Car( Robot ) :

    # 생성자.
    def __init__(self):
        self.req_no = 0 

        self.forward_duration = 1.0
        self.rotate_duration  = 0.2    
        
        left_motor = (22, 23) # 왼쪽 모터
        right_motor = (9, 25)  # 오른쪽 모터
        
        super().__init__( left_motor, right_motor)

        self.state = State.STOP

        self.fw_led = LED( 21 ) # 주행등
        self.bw_led = LED( 20 ) # 후방등
        self.lft_led = LED( 16 ) # 좌회전등
        self.rht_led = LED( 19 ) # 우회전등

        print("A car is ready.")
    pass

    # LED 깜빡이기
    def blink_led( self, led ) :
        threading.Thread(target=self.blink_led_thread, args =( led, ) ).start()
    pass

    # LED 깜빡이기 구현
    def blink_led_thread( self, led ) :
        req_no = self.req_no 
        state = self.state
        led_on = True 
        
        duration=( 0.3, 0.3 )
        if state is State.FORWARD :
            duration = (3, 0.3)
        pass

        while( req_no is self.req_no ) :
            if led_on : 
                led.on()

                sleep( duration[0] ) 
            else :
                led.off()

                sleep( duration[1] ) 
            pass 
            led_on = not led_on 
        pass
    pass

    # 공통 프로세스
    def proc_common(self):
        self.req_no += 1

        req_no = self.req_no

        state = self.state

        self.move_common( req_no, state )
    pass

    def move_common(self, req_no, state) :
        target = None

        if state is State.FORWARD :
            target = self.move_forward_thread 

            self.blink_led( self.fw_led )
        elif state is State.BACKWARD :
            target = self.move_backward_thread

            self.blink_led( self.bw_led )
        elif state is State.LEFT :
            target = self.move_left_thread

            self.blink_led( self.lft_led )
        elif state is State.RIGHT :
            target = self.move_right_thread

            self.blink_led( self.rht_led )
        elif state is State.STOP :
            pass
        pass

        if target : 
            threading.Thread(target=target, args =(req_no,)).start()
        pass
    pass

    # 전진 스레드
    def move_forward_thread(self, req_no) : 
        self.move_linear_thread( req_no, super().forward, self.forward_duration )
    pass

    # 전진 스레드
    def move_backward_thread(self, req_no) : 
        self.move_linear_thread( req_no, super().backward, self.forward_duration )
    pass

    # 좌회전 스레드
    def move_left_thread(self, req_no) : 
        self.move_linear_thread( req_no, super().left, self.rotate_duration )
    pass

    # 우회전 스레드
    def move_right_thread(self, req_no) : 
        self.move_linear_thread( req_no, super().right, self.rotate_duration )
    pass

    # 전후진 공통 스레드
    def move_linear_thread(self, req_no, move_fun, duration = 1.0) : 
        sleep_sec = 0.095 

        speed = 1.0

        pi = math.pi
        idx = 0 

        start = time.time()
        while req_no is self.req_no :
            now = time.time()
            elapsed = now - start
            
            if not idx : 
                speed = 1.0
            elif elapsed >= duration :
                speed = 0.0
            else :
                speed = math.cos( pi*elapsed/duration/2.0 )
            pass 

            print( "[%03d] elapsed = %2.4f  speed = %2.4f" % ( idx, elapsed, speed ) )  

            if speed < 0 :
                speed = 0
            pass
            
            if speed : 
                move_fun(speed)

                sleep( sleep_sec ) 
            else :
                req_no = -1 
                self.stop()
            pass

            idx += 1
        pass
    pass
    # -- move_forward_thread 

    # 모든 LED 등을 끈다.
    def turn_off_all( self ) :
        self.fw_led.off()
        self.bw_led.off()
        self.lft_led.off()
        self.rht_led.off()
    pass

    # 전진
    def forward(self, speed=1):
        self.state = State.FORWARD

        super().forward(speed)
        self.turn_off_all()
        self.fw_led.on() 

        self.proc_common()
    pass

    # 후진
    def backward(self, speed=1):
        self.state = State.BACKWARD

        super().backward(speed)
        self.turn_off_all()
        self.bw_led.on()

        self.proc_common() 
    pass

    # 좌회전
    def left(self, speed=1):
        self.state = State.LEFT
        
        super().left( speed )
        self.turn_off_all()
        self.lft_led.on()

        self.proc_common() 
    pass

    # 우회전
    def right(self, speed=1):
        self.state = State.RIGHT

        super().right( speed )
        self.turn_off_all()
        self.rht_led.on()

        self.proc_common() 
    pass

    # 뒤로 
    def reverse(self):
        self.state = State.REVERSE
        
        self.proc_common()

        super().reverse()
        self.turn_off_all()
        self.bw_led.off()

        self.proc_common() 
    pass

    # 멈춤.
    def stop(self):
        self.state = State.STOP

        super().stop()
        self.turn_off_all() 

        print( "STATE = %s" % self.state )

        self.proc_common() 
    pass 

pass

# -- car

# camera
import cv2
import numpy as np
print( "# OpenCV version %s" % cv2.__version__ )

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 24)
        self.video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'X264'))
    pass
    
    def __del__(self):
        self.video.release()
    pass

    # convert readible angle degree
    def degree( self, angle_deg ) :
        angle_deg = angle_deg % 360
        if angle_deg > 180 :
            angle_deg = angle_deg - 360
        pass

        return angle_deg
    pass 
    
    # get video frame
    def get_frame(self):
        global ads
        car = ads.car 
        gps = ads.gps

        success, img = self.video.read()

        if not success :
            h = 480
            w= 640
            # black blank image
            img = np.zeros(shape=[h, w, 3], dtype=np.uint8)
            pass 
        pass

        img = cv2.flip( img, 0 )
        h, w, _ = img.shape # image height, width 

        #print( "h = %d, w= %d" % ( h, w ))

        x = 10   # text x position
        y = 20   # text y position
        h = 20   # line height

        msg = gps.msg
                
        if not msg :
            txt = "No GPS"
        else :  
            txt = "[%06d] GPS %s %s  %s %s  %s%s H" % ( msg.gps_parse_cnt, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units )
        pass

        txt += "   " + car.state
        self.putTextLine( img, txt , x, y ) 

        # gyro angle text drawing
        imu = ads.berryIMU
        x = 10
        y += h

        imuData = imu.imuData
        
        txt = ""
        format = "[%06d] GyroAngle X %+06.2f   Y %+06.2f   Z %+06.2f   (deg)"
        txt +=  format % (imuData.imu_cnt, self.degree( imuData.gyroXangle ), self.degree( imuData.gyroYangle ), self.degree( imuData.gyroZangle ) ) 
        self.putTextLine( img, txt , x, y ) 

        # pitch, roll, yaw drawing
        x = 10
        y += h
        format = "[%06d] Pitch % 5.2f   Roll % 5.2f   Yaw % 5.2f   (deg)"
        txt = format % ( imuData.imu_cnt, self.degree( imuData.pitch_deg ), self.degree( imuData.roll_deg ), self.degree( imuData.yaw_deg ) )
        self.putTextLine( img, txt , x, y ) 

        # kalman x, y drawing
        x = 10
        y += h
        format = "[%06d] Kalman X % 5.2f   Y % 5.2f "
        txt = format % ( imuData.imu_cnt, imuData.kalmanX, imuData.kalmanY )
        self.putTextLine( img, txt , x, y ) 

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the video stream.
        ret, jpeg = cv2.imencode('.jpg', img)
        
        return jpeg.tobytes()
    pass

    # opencv 이미지에 텍스트를 그린다.
    def putTextLine(self, img, txt, x, y ) :
        font = cv2.FONT_HERSHEY_SIMPLEX # font
        fs = 0.4  # font size(scale)
        ft = 1    # font thickness
        

        bg_color = (255, 255, 255) # text background color
        fg_color = (255,   0,   0) # text foreground color

        cv2.putText(img, txt, (x, y), font, fs, bg_color, ft + 2, cv2.LINE_AA)
        cv2.putText(img, txt, (x, y), font, fs, fg_color, ft    , cv2.LINE_AA) 
    pass
pass

# -- camera

# web by flask framewwork
from flask import Flask, render_template, Response, jsonify
from flask import request 

from BerryIMU import *

class AdsSystem :
    def __init__( self ) :
        self.init = 0 
        self.gps = Gps()
        self.camera = Camera()
        self.car = Car()
        self.berryIMU = BerryIMU()
        self.req_no = 0
    pass

    def initSystem(self) : 
        if not self.init :
            self.init = 1
            self.gps.read_gps_thread()
            self.berryIMU.read_imu_thread()
            self.init = 2
        pass
    pass
pass

ads = None 

def init_system() :
    global ads
    if not ads :
        ads = AdsSystem()
        ads.initSystem()
    pass 
pass

app = Flask(__name__)

def gen(camera):
    global ads 
    while True:
        frame = ads.camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    pass
pass 

@app.route( '/' )
@app.route( '/index.html' )
@app.route( '/index.htm' )
def index():
    init_system()
    return render_template('index.html')
pass

@app.route('/info.html')
def info():
    init_system()
    return render_template('info.html')
pass

@app.route('/video_feed')
def video_feed():
    init_system()
    return Response(gen(ads.camera), mimetype='multipart/x-mixed-replace; boundary=frame')
pass

@app.route('/car.json') 
def car_json():
    global ads
    car = ads.car
    ads.req_no += 1
    motion = request.args.get('motion')

    print( "motion = %s" % motion )

    if "forward" == motion :
        car.forward() 
    elif "backward" == motion :
        car.backward() 
    elif "left" == motion :
        car.left() 
    elif "right" == motion  :
        car.right() 
    else:
        car.stop() 
    pass

    return jsonify(
            motion=motion,
            req_no = ads.req_no,
        )
pass

# -- web by flask framewwork

if __name__ == '__main__':
    use_ssl = 0
    if use_ssl : 
        app.run(host='0.0.0.0', port=443, ssl_context='adhoc', debug=True)
    else :
        app.run(host='0.0.0.0', port=80, debug=True)
    pass
pass
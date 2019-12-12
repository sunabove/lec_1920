# coding: utf-8

def check_pkg( pkg ) : 
	try:
		import importlib
		mode_name = pkg.split(",")[0].strip() 
		importlib.import_module( mode_name )
	except ModuleNotFoundError :
		print( '%s is not installed, installing it now ... ' % mode_name )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg.split(",")[-1].strip() ] )
	pass
pass

for pkg in [ "flask", "flask_socketio", "OpenSSL, pyopenssl", "serial, pyserial", "pynmea2" ] :
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
        self.dbg = 0
        self.gps_cnt = 0 
        self.gps_parse_cnt = 0 
        self.msg = None
        self.curr_msg = None  
    pass

    def parseGPS(self, str):
        if 'GGA' in str :
            msg = pynmea2.parse(str) 

            if msg.lat :
                self.gps_parse_cnt += 1

                self.curr_msg = msg
            pass

            gps_parse_cnt = self.gps_parse_cnt 
            
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
    MOVE = "MOVE"
pass
    
from gpiozero import Robot, LED

class Car( Robot ) :

    # 생성자.
    def __init__(self):
        self.req_no = 0 

        self.forward_duration = 1.0
        self.rotate_duration  = 0.2    

        self.pitchDeg = 0 
        self.rollDeg = 0 
        
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
        if state in( State.FORWARD, State.MOVE ) :
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

        if state is State.MOVE :
            target = self.move_thread 
        elif state is State.FORWARD :
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
            # To filter out finished threads
            #threads = [t for t in threads if t.is_alive()]

            threading.Thread(target=target, args=(req_no,)).start()
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
                speed = math.sin( pi*(elapsed + sleep_sec)/duration )
                #speed = math.cos( pi*elapsed/duration/2.0 )
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

    # 이동 스레드
    def move_thread(self, req_no ) : 
        '''
            if (15 <= roll) {
                motion = Motion.RIGHT ;
            } else if ( -15 >= roll) {
                motion = Motion.LEFT ;
            } else if ( 45 <= pitch) {
                motion = Motion.FORWARD ;
            } else if ( 32 >= pitch) {
                motion = Motion.BACKWARD ;
            } else {
                motion = Motion.STOP ;
            }
        '''
        
        sleep_sec = 0.095  
        idx = 0 

        start = time.time()
        while req_no is self.req_no :
            now = time.time()
            elapsed = now - start 

            pitch = self.pitchDeg
            roll = self.rollDeg

            speed  = 0.3

            if 32 >= pitch :
                speed = pitch/90.0
                super().backward( speed )

                print( "[%03d] move back elapsed = %2.4f  speed = %2.4f" % ( idx, elapsed, speed ) )  

                self.blink_led( self.bw_led )
            elif 180 < roll :
                speed = pitch/90.0
                curve_left = (360 - roll)/180.0
                super().forward(speed, curve_left = curve_left)

                print( "[%03d] move left elapsed = %2.4f  speed = %2.4f, curve_left = %2.4f" % ( idx, elapsed, speed, curve_left ) )  
                
                self.blink_led( self.lft_led )
            elif 180 > roll :
                speed = pitch/90.0
                curve_right  = roll/180.0
                super().forward(speed, curve_right = curve_right)

                print( "[%03d] move right elapsed = %2.4f  speed = %2.4f, curve_right = %2.4f" % ( idx, elapsed, speed, curve_right ) )  

                self.blink_led( self.rht_led )
            pass

            sleep( sleep_sec ) 

            idx += 1
        pass
    pass
    # -- move thread 

    # 모든 LED 등을 끈다.
    def turn_off_all( self ) :
        self.fw_led.off()
        self.bw_led.off()
        self.lft_led.off()
        self.rht_led.off()
    pass

    # 이동
    def move(self, pitchDeg, rollDeg ):

        self.state = State.MOVE
        self.pitchDeg = pitchDeg 
        self.rollDeg = rollDeg 

        super().forward( 0.3 )
        self.turn_off_all()
        self.fw_led.on() 

        self.proc_common()
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

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 15)
        self.video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'X264'))
    pass
    
    def __del__(self):
        self.video.release()
    pass

    # convert readible angle degree
    def pretty_angle( self, angle_deg ) :
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
            format = "[%06d] GPS %s %s  %s %s  %s%s H" 

            txt = format % ( msg.gps_parse_cnt, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units )
        pass

        txt += "   " + car.state
        self.putTextLine( img, txt , x, y ) 

        imu = ads.berryIMU
        
        imuData = imu.imuData

        txt = ""

        # gyro angle text drawing
        if 0 : 
            x = 10
            y += h
            format = "[%06d] GyroAngle Y(Pitch) %+06.2f   X(Roll) %+06.2f   Z(Yaw) %+06.2f   (deg)"
            txt +=  format % (imuData.imu_cnt, self.pretty_angle( imuData.gyroYangle ), self.pretty_angle( imuData.gyroXangle ), self.pretty_angle( imuData.gyroZangle ) ) 
            self.putTextLine( img, txt , x, y ) 
        pass

        # pitch, roll, yaw drawing
        x = 10
        y += h
        format = "[%06d] Pitch % 5.2f   Roll % 5.2f   Yaw % 5.2f   (deg)"
        txt = format % ( imuData.imu_cnt, self.pretty_angle( imuData.pitch_deg ), self.pretty_angle( imuData.roll_deg ), self.pretty_angle( imuData.yaw_deg ) )
        self.putTextLine( img, txt , x, y ) 

        # kalman x, y drawing
        x = 10
        y += h
        format = "[%06d] Kalman X % 5.2f   Y % 5.2f "
        txt = format % ( imuData.imu_cnt, imuData.kalmanX, imuData.kalmanY )
        self.putTextLine( img, txt , x, y ) 

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the video stream.
        _, jpg = cv2.imencode('.jpg', img) 
        
        return jpg.tobytes()
    pass

    # opencv 이미지에 텍스트를 그린다.
    def putTextLine(self, img, txt, x, y ) :
        # /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf
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
            print( "# System initiating ...")

            print( "# OpenCV version %s" % cv2.__version__ )

            self.init = 1
            self.gps.read_gps_thread()
            self.berryIMU.read_imu_thread()
            self.init = 2

            print( "# System is initiated.\n")
        pass
    pass
pass

ads = None 

app = Flask(__name__)

def init_system():
    global ads
    if not ads :
        ads = AdsSystem()
        ads.initSystem()
    pass 
pass 

def gen(camera):
    global ads 
    while True:
        frame = ads.camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    pass
pass 

@app.before_first_request
def activate_job():
    init_system()
pass

@app.route( '/' )
@app.route( '/index.html' )
@app.route( '/index.htm' )
def index(): 
    return render_template('index.html')
pass

@app.route('/info.html')
def info(): 
    return render_template('info.html')
pass

@app.route('/video_feed')
def video_feed(): 
    return Response(gen(ads.camera), mimetype='multipart/x-mixed-replace; boundary=frame')
pass

@app.route('/car.json') 
def car_json():
    global ads
    car = ads.car
    ads.req_no += 1
    motion = request.args.get('motion').lower()

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

@app.route('/car_move.json') 
def car_move_json():
    global ads
    car = ads.car
    ads.req_no += 1
    motion = request.args.get('motion').lower()

    pitchDeg = float( request.args.get('pitchDeg').lower() ) % 360
    rollDeg = float( request.args.get('rollDeg').lower() ) % 360

    print( "car_move motion = %s" % motion )

    print( "car_move motion = %s" % motion )

    if "stop" == motion :
        car.stop()  
    else:
        car.move( pitchDeg, rollDeg ) 
    pass

    return jsonify(
            motion=motion,
            req_no = ads.req_no,
        )
pass

@app.route('/send_me_curr_pos.json')
def send_me_curr_pos_json(): 
    
    if ads.init < 2 :
        return { "valid" : 0 }, 200
    pass

    json = self.get_curr_pos_json()

    return json, 200
pass 

def get_curr_pos_json():
    curr_msg = ads.gps.curr_msg 

    if not curr_msg :
        return { "valid" : 0 }, 200
    pass

    yaw_deg = -1
    imu = ads.berryIMU
    if imu : 
        imuData = imu.imuData
        if imuData : 
            yaw_deg = imuData.yaw_deg
            yaw_deg = yaw_deg % 360
        pass
    pass

    json = {
        "valid" : 1, 
        "gps_parse_cnt" : "%s" % curr_msg.gps_parse_cnt, 
        "timestamp" : "%s" % curr_msg.timestamp,
        "latitude" : "%s" % curr_msg.latitude,
        "longitude" : "%s" % curr_msg.longitude, 
        "altitude" : "%s" %  curr_msg.altitude,
        "heading" : "%s" % yaw_deg,
    }

    return json
pass

# -- web by flask framewwork  

# socket io

from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@app.route('/socket.html')
def socket_test():
    return render_template('websocket-index.html' )
pass

slider_cnt = 0 
socket_cnt = 0 

@socketio.on('Slider value changed')
def slider_value_changed(message):
	global slider_cnt
	slider_cnt += 1
	print( "[%04d] Slider value changed" % slider_cnt ) 
	emit('update value', slider_cnt, broadcast=True)
pass 

@socketio.on('connect')
def socket_connect():
    print( "socket connected." )

    emit( 'send_me_curr_pos',  1 )
pass

@socketio.on('send_me_curr_pos')
def send_me_curr_pos(message):
    global socket_cnt
    socket_cnt += 1
    print( "[%04d] send_me_curr_pos" % socket_cnt ) 

    json = get_curr_pos_json() 

    emit( 'send_me_curr_pos', json, broadcast=True)
pass

# -- socket io 

if __name__ == '__main__':
    use_ssl = 0
    use_socket = 1 

    if use_socket :
        print( "## SocketIO Web")
        socketio.run(app, host='0.0.0.0', port=80, debug=True)
    elif use_ssl : 
        print( "## SSL WEB ")
        app.run(host='0.0.0.0', port=443, ssl_context='adhoc', debug=True, threaded=True)
    else :
        print( "## Normal WEB")
        app.run(host='0.0.0.0', port=80, debug=True, threaded=True) 
    pass 
pass
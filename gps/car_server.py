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

for pkg in [ "flask", "geopy", "flask_socketio", "OpenSSL, pyopenssl", "serial, pyserial", "pynmea2" ] :
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
import geopy 
import geopy.distance

class Gps : 
    def __init__(self):
        self.dbg = 0
        self.gps_cnt = 0 
        self.gps_parse_cnt = 0 
        self.msg = None
        self.msg_list = []
        self.msg_curr = None  
        self.msg_prev = None 
    pass

    def calculate_compass_bearing(self, point_a, point_b):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),
                    cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
        - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
        - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
        The bearing in degrees
        :Returns Type:
        float
        """
        if (type(point_a) != tuple) or (type(point_b) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(point_a[0])
        lat2 = math.radians(point_b[0])

        diffLong = math.radians(point_b[1] - point_a[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360 

        return compass_bearing
    pass
    # -- calculate_compass_bearing

    def get_heading_current( self ) :
        msg_curr = self.msg_curr 
        msg_prev = self.msg_prev
        

        if not msg_curr or not msg_prev :
            return -1 
        pass 

        msg_list = self.msg_list

        idx = len( msg_list ) - 2 

        latLngCurr = ( msg_curr.latitude, msg_curr.longitude )

        while -1 < idx :
            msg = msg_list[ idx ] 
            latLng = ( msg.latitude, msg.longitude )
            dist = geopy.distance.vincenty( latLngCurr, latLng ).meters

            if 0.01 < dist or 0 is idx : 
                compass_bearing = self.calculate_compass_bearing( latLngCurr, latLng )

                return compass_bearing
            pass

            idx -= 1
        pass 
    pass

    def parseGPS(self, str):
        if 'GGA' in str :
            msg = pynmea2.parse(str) 

            if msg.lat :
                self.gps_parse_cnt += 1

                self.msg_prev = self.msg_curr

                if not self.msg_prev :
                    self.msg_prev = msg 
                pass

                self.msg_curr = msg
                
                self.msg = msg  

                msg_list = self.msg_list 
                msg_list.append( msg )

                while 1_000 < len( msg_list ) :
                    msg_list.pop( 0 )
                pass

                gps_parse_cnt = self.gps_parse_cnt 
            
                msg.gps_parse_cnt = gps_parse_cnt 

                if self.dbg : 
                    print( "[%04d] %s" % ( gps_parse_cnt, str ) , end ="" )
                    format = "[%04d] Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" 
                    print( format % ( gps_parse_cnt, msg.timestamp, msg.lat,msg.lat_dir, msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats) )
                pass
            else :
                print( "### Invalid gps data....")
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
    
    LEFT = "LEFT"
    RIGHT = "RIGHT" 
    
    STOP = "STOP"
    REVERSE = "REVERSE"
    
    DRIVE = "DRIVE"

    AUTOPILOT = "AUTOPILOT"
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
        if state in( State.FORWARD, State.DRIVE ) :
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

        if state is State.DRIVE :
            target = self.drive_thread 
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
    def drive_thread(self, req_no ) :  
        
        sleep_sec = 0.3
        idx = 0

        prev = time.time()

        back_angle = 32.0
        curve_angle = 90.0

        while req_no is self.req_no and self.state is State.DRIVE :
            now = time.time()
            elapsed = now - prev 

            pitch = self.pitchDeg
            roll = self.rollDeg 

            leds = [ ]

            speed = pitch/90.0
            
            print( "[%03d] elapsed = %2.4f  pitch = %2.4f  roll = %2.4f " % ( idx, elapsed, pitch, roll ) )   

            if idx :
                pass
            elif 0 <= pitch <= back_angle : # 후진
                leds.append( self.bw_led ) 

                speed = 0.4 + (back_angle - pitch + 0.0)/back_angle

                if 1 < speed :
                    speed = 1
                elif 0 > speed :
                    speed = 0
                pass

                if 10 <= roll <= 180 : 
                    curve_right = roll/curve_angle
                    if 1 > curve_right :
                        curve_right = 1.0
                    pass

                    super().backward( speed , curve_right = curve_right )
                    print( "[%03d] drive back elapsed = %2.4f  speed = %2.4f  curve_right = %2.4f" % ( idx, elapsed, speed, curve_right ) )  

                    leds.append( self.lft_led )
                elif 180 <= roll <= 350 : 
                    curve_left = (360 - roll)/curve_angle

                    if 1 > curve_left :
                        curve_left = 1.0
                    pass

                    super().backward( speed , curve_left = curve_left )
                    print( "[%03d] drive back elapsed = %2.4f  speed = %2.4f  curve_left = %2.4f" % ( idx, elapsed, speed, curve_left ) )  

                    leds.append( self.rht_led )
                else :
                    super().backward( speed )
                    print( "[%03d] drive back elapsed = %2.4f  speed = %2.4f" % ( idx, elapsed, speed ) )
                pass
            else : # 전진
                leds.append( self.fw_led )

                if 10 <= roll <= 180 : 
                    curve_right = roll/curve_angle
                    if 1 > curve_right :
                        curve_right = 1.0
                    pass

                    super().forward( speed , curve_right = curve_right )
                    print( "[%03d] drive forward elapsed = %2.4f  speed = %2.4f  curve_right = %2.4f" % ( idx, elapsed, speed, curve_right ) )  

                    leds.append( self.lft_led )
                elif 180 <= roll <= 350 : 
                    curve_left = (360 - roll)/curve_angle

                    if 1 > curve_left :
                        curve_left = 1.0
                    pass

                    super().forward( speed , curve_left = curve_left )
                    print( "[%03d] drive forward elapsed = %2.4f  speed = %2.4f  curve_left = %2.4f" % ( idx, elapsed, speed, curve_left ) )  

                    leds.append( self.rht_led )
                else :
                    super().forward( speed )
                    print( "[%03d] drive forward elapsed = %2.4f  speed = %2.4f" % ( idx, elapsed, speed ) )
                pass
            pass

            value = self.value 
            print( "[%03d] drive elapsed = %2.4f  motor speed  left = %2.4f  right = %2.4f" % ( idx, elapsed, value[0], value[1] ) )

            self.turn_off_all()

            for led in leds : 
                if not idx%2 :
                    led.on()
                else :
                    led.off()
                pass
            pass

            prev = now

            sleep( sleep_sec ) 

            idx += 1
        pass
    pass
    # -- move thread 

    # 자율 주행

    def auto_pilot( self, lat, lng ) :
        target = self.auto_pilot_thread 
        req_no = self.req_no

        threading.Thread( target=target, args=( req_no, lat, lng, ) ).start()
    pass

    # 이동 스레드
    def auto_pilot_thread(self, req_no, lat, lng ) :  
        sleep_sec = 0.1
        idx = 0

        prev = time.time() 

        gps = ads.gps

        latLng_goal = ( lat, lng )

        heading_diff_prev = None
        curve_right = 0
        curve_left  = 0 

        while req_no is self.req_no  and self.state is State.AUTOPILOT :
            now = time.time()
            elapsed = now - prev  

            speed = 0.7

            leds = [ ] 

            msg = gps.msg_curr

            latLng_curr = ( msg.latitude, msg.longitude )

            heading_goal = ads.gps.calculate_compass_bearing( latLng_curr, latLng_goal )
            heading_curr = ads.gps.get_heading_current()

            heading_diff = heading_goal - heading_curr
            heading_diff = heading_diff % 360 

            if 5 < abs( heading_diff ) : 
                if heading_diff_prev is None :
                    heading_diff_prev = heading_diff
                else :
                    if 0 < heading_diff : 
                        curve_right = 0.7 
                        super().forward( speed, curve_right = curve_right )
                    else :
                        curve_left  = 0.7 
                        super().forward( speed, curve_left  = curve_left  )
                    pass

                    heading_diff_prev = heading_diff
                pass
            else :
                heading_diff_prev = None
                curve_right = 0
                curve_left  = 0 
            pass

            value = self.value 
            print( "[%03d] autopilot elapsed = %2.4f  motor speed  left = %2.4f  right = %2.4f" % ( idx, elapsed, value[0], value[1] ) )

            self.turn_off_all()

            for led in leds : 
                if not idx%2 :
                    led.on()
                else :
                    led.off()
                pass
            pass

            prev = now

            sleep( sleep_sec ) 

            idx += 1
        pass
    pass
    # -- autopilot thread 

    # -- 자율 주행 

    # 모든 LED 등을 끈다.
    def turn_off_all( self ) :
        self.fw_led.off()
        self.bw_led.off()
        self.lft_led.off()
        self.rht_led.off()
    pass

    # 운전하기 
    def drive(self, pitchDeg, rollDeg ):

        self.state = State.DRIVE
        self.pitchDeg = pitchDeg 
        self.rollDeg = rollDeg 

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
            heading = gps.get_heading_current()
            if not heading : 
                heading = "None"
            else :
                heading = "%3.2f" % self.pretty_angle( heading )
            pass

            format = "[%06d] GPS %s %s  %s %s  %s%s H %s" 

            txt = format % ( msg.gps_parse_cnt, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, heading )
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

@app.route('/car_drive.json') 
def car_drive_json():
    global ads
    car = ads.car
    ads.req_no += 1
    motion = request.args.get('motion').lower()

    print( "car_move motion = %s" % (motion ) ) 

    if "autopilot" == motion :
        lat = float( request.args.get('lat') ) 
        lng = float( request.args.get('lng') ) 

        print( "car_move motion = %s, lat = %f, long = %f" % (motion, lat, lng ) ) 

        car.auto_pilot( lat, lng )
    elif "stop" == motion :
        car.stop()  
    elif "left" == motion :
        car.left()  
    elif "right" == motion :
        car.right()   
    elif "forward" == motion :
        car.forward()   
    elif "backward" == motion :
        car.backward()   
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

    yaw_deg = -1
    imu = ads.berryIMU
    if imu : 
        imuData = imu.imuData
        if imuData : 
            yaw_deg = imuData.yaw_deg
            yaw_deg = yaw_deg % 360
        pass
    pass

    msg_curr = ads.gps.msg_curr 

    if not msg_curr :
        return { "valid" : 0 }, 200
    pass

    json = {
        "valid" : 1, 
        "gps_parse_cnt" : "%s" % msg_curr.gps_parse_cnt, 
        "timestamp" : "%s" % msg_curr.timestamp,
        "latitude" : "%s" % msg_curr.latitude,
        "longitude" : "%s" % msg_curr.longitude, 
        "altitude" : "%s" %  msg_curr.altitude,
        "heading" : "%s" % yaw_deg,
    }

    return json, 200
pass

# -- web by flask framewwork   

if __name__ == '__main__':
    use_ssl = 0
    use_socket = 1 

    if use_ssl : 
        print( "## SSL WEB ")
        app.run(host='0.0.0.0', port=443, ssl_context='adhoc', debug=True, threaded=True)
    else :
        print( "## Normal WEB")
        app.run(host='0.0.0.0', port=80, debug=True, threaded=True) 
    pass 
pass
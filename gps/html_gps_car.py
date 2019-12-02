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

for pkg in [ "serial, pyserial", "pynmea2" ] :
	check_pkg( pkg )
pass

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# gps

import serial
import pynmea2

class Gps : 
    def __init__(self):
        self.gps_serial = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 20 )
        self.gps_parse_cnt = 0
        self.lat = 0
        self.lon = 0
        self.alt = 0 
    pass

    def parseGPS(self, str):
        if 'GGA' in str :
            self.gps_parse_cnt += 1
            gps_parse_cnt = self.gps_parse_cnt
            msg = pynmea2.parse(str)
            if 1 : 
                print( "[%04d] %s" % ( gps_parse_cnt, str ) , end ="" )
                print( "[%04d] Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % ( gps_parse_cnt, msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats) )
            pass
            self.lat = msg.lat
            self.lon = msg.lon
            self.alt = msg.altitude 
        pass
    pass 

    def read_gps_thread(self) :
        from threading import Thread
        Thread(target=self.read_gps_impl ).start()
        pass
    pass

    def read_gps_impl(self) :
        while 1 :  
            try : 
                gps_serial =self.gps_serial
                while 1 :
                    str = gps_serial.readline()
                    self.parseGPS(str.decode( "utf-8"))
                pass
            except Exception as e:
                print( str(e) )
                print( "Serial Device Error" )
                #import time
                #time.sleep( 1 )
            pass
        pass
    pass 
pass

# -- gps

# car

from gpiozero import Robot, LED

class Car( Robot ) :

    def __init__(self, left, right, *, pwm=True, pin_factory=None):
        print("A car is ready.")
        super().__init__( left, right, pwm, pin_factory )

        self.state = "STOP"

        self.fw_led = LED( 21 ) # 주행등
        self.bw_led = LED( 20 ) # 후방등
        self.lft_led = LED( 16 ) # 좌회전등
        self.rht_led = LED( 19 ) # 우회전등
    pass

    def turn_off_all( self ) :
        self.fw_led.off()
        self.bw_led.off()
        self.lft_led.off()
        self.rht_led.off()
    pass

    def forward(self, speed=1):
        super().forward(speed)
        self.turn_off_all()
        self.fw_led.on() 

        self.state = "FORWARD" 
    pass

    def backward(self, speed=1):
        super().backward(speed)
        self.turn_off_all()
        self.bw_led.on()

        self.state = "BACKWARD" 
    pass

    def left(self, speed=1):
        super().left( speed )
        self.turn_off_all()
        self.lft_led.on()

        self.state = "LEFT" 
    pass

    def right(self, speed=1):
        super().right( speed )
        self.turn_off_all()
        self.rht_led.on()

        self.state = "RIGHT" 
    pass

    def reverse(self):
        super().reverse()
        self.turn_off_all()
        self.bw_led.off()

        self.state = "REVERSE" 
    pass

    def stop(self):
        super().stop()
        self.turn_off_all()
        self.state = "STOP" 
    pass 

pass

# -- car

# camera
import cv2

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, img = self.video.read()
        global ads
        car = ads.car 

        img = cv2.flip( img, 0 )
        h, w, _ = img.shape
        font = cv2.FONT_HERSHEY_SIMPLEX ; fs = 0.5; ft = 1
        x = 10
        y = 20
        cv2.putText(img, car.state, (x, y), font, fs, (255,255,255), ft, cv2.LINE_AA)

        if 0 : 
            logging.debug( 'width: %d' % w)
            logging.debug( 'height: %d' % h)
        pass
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
    pass
pass

# -- camera

# web by flask framewwork
from flask import Flask, render_template, Response, jsonify
from flask import request 

class AdsSystem :
    def __init__( self ) :
        self.gps = Gps()
        self.camera = Camera()
        self.car = Car(left=(22, 23), right=(9, 25))
        self.req_no = 0
    pass

    def initSystem(self) : 
        self.gps.read_gps_thread()
    pass
pass

ads = None 
app = Flask(__name__)

def init_system() :
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

@app.route('/')
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
    ads.req_no += 1
    motion = request.args.get('motion')

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
            req_no = req_no,
        )
pass

# -- web by flask framewwork

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
pass
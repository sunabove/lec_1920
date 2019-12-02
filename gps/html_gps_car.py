# coding: utf-8

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

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

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image = cv2.flip( image, 0 )
        h, w, _ = image.shape
        logging.debug( 'width: %d' % w)
        logging.debug( 'height: %d' % h)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    pass
pass

# -- camera

# web by flask framewwork
from flask import Flask, render_template, Response, jsonify
from flask import request 

car = None
camera = None
req_no = 0
app = Flask(__name__)

def init_system() :
    global car
    if not car :
        car = Car(left=(22, 23), right=(9, 25))
    pass

    global camera
    if not camera :
        camera = VideoCamera()
    pass
pass

@app.route('/')
def index():
    init_system()
    return render_template('index.html')
pass

@app.route('/info.html')
def info():
    init_system
    return render_template('info.html')
pass

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    pass
pass

@app.route('/video_feed')
def video_feed():
    init_system()
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
pass

@app.route('/car.json') 
def car_json():
    global req_no
    req_no += 1
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
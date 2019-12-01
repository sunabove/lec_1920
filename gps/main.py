# coding: utf-8

import logging

from flask import Flask, render_template, Response, jsonify
from flask import request
from camera import VideoCamera

# car

from gpiozero import Robot, LED

class Car( Robot ) :

    def __init__(self, left, right, *, pwm=True, pin_factory=None):
        print("A car is ready.")
        super().__init__( left, right, pwm, pin_factory )

        self.camera = None 
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
        self.paint()       
    pass

    def backward(self, speed=1):
        super().backward(speed)
        self.turn_off_all()
        self.bw_led.on()

        self.state = "BACKWARD"
        self.paint() 
    pass

    def left(self, speed=1):
        super().left( speed )
        self.turn_off_all()
        self.lft_led.on()

        self.state = "LEFT"
        self.paint() 
    pass

    def right(self, speed=1):
        super().right( speed )
        self.turn_off_all()
        self.rht_led.on()

        self.state = "RIGHT"
        self.paint() 
    pass

    def reverse(self):
        super().reverse()
        self.turn_off_all()
        self.bw_led.off()

        self.state = "REVERSE"
        self.paint() 
    pass

    def stop(self):
        super().stop()
        self.turn_off_all()
        self.state = "STOP"
        self.paint() 
    pass

    def paint(self) :
        if self.camera : 
            self.camera.annotate_text = self.state
        pass
    pass

pass

# -- car

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
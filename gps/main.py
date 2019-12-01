# coding: utf-8
#  
from flask import Flask, render_template, Response, jsonify
from camera import VideoCamera

camera = None
req_no = 0
app = Flask(__name__)

def init_system() :
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
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
pass

@app.route('/car.json') 
def car_json():
    global req_no
    req_no += 1
    motion = "STOP"
    return jsonify(
            req_no = req_no,
            motion=motion
        )
pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
#!/usr/bin/python3
# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

def check_pkg( pkg ) : 
	try:
		import importlib
		importlib.import_module( pkg.split(",")[0] )
	except ModuleNotFoundError :
		print( '%s is not installed, installing it now!' % pkg )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg.split(",")[-1] ] )
	pass
pass

for pkg in [ "picamera", "RPi.GPIO", "gpiozero" ] :
	check_pkg( pkg )
pass

# car

from gpiozero import Robot, LED

class Car( Robot ) :

    def __init__(self, left, right, *, pwm=True, pin_factory=None):
        print("A car is ready.")
        super().__init__( left, right, pwm, pin_factory )

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
    pass

    def backward(self, speed=1):
        super().backward(speed)
        self.turn_off_all()
        self.bw_led.on()
    pass

    def left(self, speed=1):
        super().left( speed )
        self.turn_off_all()
        self.lft_led.on()
    pass

    def right(self, speed=1):
        super().right( speed )
        self.turn_off_all()
        self.rht_led.on()
    pass

    def reverse(self):
        super().reverse()
        self.turn_off_all()
        self.bw_led.off()
    pass

    def stop(self):
        super().stop()
        self.turn_off_all()
    pass

pass

car = Car(left=(22, 23), right=(9, 25))

# -- car

import io
import logging
import socketserver
from threading import Condition
from http import server

page = { 
"root" : 
"""\
<!DOCTYPE html>
<html>
<head> 
</head>
<body>
<iframe src="stream.html" style="display:block; width:100%; height:95vh;" frameborder="0" ></iframe>
<iframe name="action" src="about:blank" width="100%" height="30" frameborder="0" style="border: 1px solid black;"></iframe>
</body>
</html>
""",

"index" : 
"""\
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Raspberry Pi Camera</title>
    <style>
        form, input { display: inline; font-size: 24px; }
    </style>
</head>
<body>
<center><img src="stream.mjpg" ></center>
<br/>
<center>
    <table style="text-align: center;" border="0" >
        <tr>
            <td></td>
            <td>
                <form target="action" action="car.json" >
                    <input type="hidden" name="forward" value="1" />
                    <input type="submit" value="&nbsp; &uarr; &nbsp;" />
                </form>
            </td>
            <td></td>
        </tr>
        <tr>
            <td>
                <form target="action" action="car.json" >
                    <input type="hidden" name="left" value="1" />
                    <input type="submit" value="&nbsp; &larr; &nbsp;" />
                </form>
            </td>
            <td>
                <form target="action" action="car.json" >
                    <input type="hidden" name="stop" value="1" />
                    <input type="submit" value="&nbsp; &bull; &nbsp;" />
                </form>
            </td>
            <td>
                <form target="action" action="car.json" >
                    <input type="hidden" name="right" value="1" />
                    <input type="submit" value="&nbsp; &rarr; &nbsp;" />
                </form>
            </td>
        </tr>
        <tr>
            <td></td>
            <td>
                <form target="action" action="car.json" >
                    <input type="hidden" name="backward" value="1" />
                    <input type="submit" value="&nbsp; &darr; &nbsp;" />
                </form>
            </td>
            <td></td>
        </tr>
    </table>
</center>
</body>
</html>
""" 
    } 

class RequestHandler(server.BaseHTTPRequestHandler):

    car_req_no = 0 

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        print( "RequestHandler inited." )
    pass

    def do_GET(self):
        path = self.path
        logging.info( "path: %s" % path )
        if path in ( "", "/", "/index.html" ):
            content = page["root"].encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif "car.json" in path :

            motion = "" 

            if "forward" in path :
                car.forward()
                motion = "forward" 
            elif "backward" in path :
                car.backward()
                motion = "backward" 
            elif "left" in path :
                car.left()
                motion = "left" 
            elif "right" in path :
                car.right()
                motion = "right" 
            else:
                car.stop()
                motion = "stop" 
            pass

            RequestHandler.car_req_no += 1
            content = "car json [%d] : %s" % ( RequestHandler.car_req_no, motion )
            content = content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif path == '/stream.html':
            content = page["index"].encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    pass
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                pass
            except Exception as e:
                logging.warning( 'Removed streaming client %s: %s', self.client_address, str(e))
            pass
        else:
            self.send_error(404)
            self.end_headers()
        pass
    pass
pass

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    pass

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
    pass
pass

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
pass

import picamera 

with picamera.PiCamera( resolution='640x480', framerate=24 ) as camera:
    output = StreamingOutput()
    camera.rotation = 180 #Camera rotation in degrees
    camera.start_recording(output, format='mjpeg')
    try:
        server = StreamingServer(('', 80), RequestHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
    pass
pass


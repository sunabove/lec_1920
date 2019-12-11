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

for pkg in [ "flask", "flask_socketio", "eventlet" ] :
	check_pkg( pkg )
pass

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('websocket-index.html',**values)
pass

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})
pass

slider_cnt = 0 

@socketio.on('Slider value changed')
def value_changed(message):
	global slider_cnt
	slider_cnt += 1
	print( "[%04d] Slider value changed" % slider_cnt )
	values[message['who']] = message['data']
	emit('update value', message, broadcast=True)
pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
pass
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
from flask_socketio import SocketIO, join_room, emit 

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('flask-websocket-index.html')

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""  
    emit('join_room', {'room': 1})

if __name__ == '__main__':
    socketio.run(app, debug=True)
pass
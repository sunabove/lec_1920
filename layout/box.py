# coding: utf-8
def check_pkg( pkg ) : 
	try:
		import importlib
		importlib.import_module( pkg )
	except ModuleNotFoundError :
		print( '%s package is not installed, installing it now ...' % pkg )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg ] )
	pass
pass

for pkg in [ "guizero" ] :
	check_pkg( pkg )
pass

from guizero import App, Box, Text
app = App(title="My app", height=300, width=400)
box = Box(app)
text1 = Text(box, text="Hello from the box", size=14, color="red", font="Arial")
text2 = Text(app, text="Hello from the app", size=14, color="blue", font="Courier New")
app.display()

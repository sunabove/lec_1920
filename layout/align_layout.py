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

from guizero import App, Text
app = App()
top_text = Text(app, text="at the top", align="top")
bottom_text = Text(app, text="at the bottom", align="bottom")
left_text = Text(app, text="to the left", align="left")
right_text = Text(app, text="to the right", align="right")
app.display()

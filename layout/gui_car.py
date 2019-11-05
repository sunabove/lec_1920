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

from guizero import *
app = App()

box = Box(app, width="fill", height="fill" )

top_text = Text(box, text="at the top", align="left")
picture1 = Picture(box, image="std1.gif", grid=[0,0] )
left_text = Text(box, text="to the left", align="right")

status = Text(app, text="to the right", align="bottom")

app.display()

# coding: utf-8
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

for pkg in [ "gpiozero", "PIL,Pillow" ] :
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
    pass

    def forward(self, speed=1):
        super().forward(speed)
        self.fw_led.on()
        self.bw_led.off()
    pass

    def backward(self, speed=1):
        super().backward(speed)
        self.fw_led.off()
        self.bw_led.on()
    pass

    def left(self, speed=1):
        super().left( speed )
        self.fw_led.off()
        self.bw_led.off()
    pass

    def right(self, speed=1):
        super().right( speed )
        self.fw_led.off()
        self.bw_led.off()
    pass

    def reverse(self):
        super().reverse()
        self.fw_led.off()
        self.bw_led.off()
    pass

    def stop(self):
        super().stop()
        self.fw_led.off()
        self.bw_led.off()
    pass

pass

car = Car(left=(22, 23), right=(9, 25))

# -- car

# video open
print( "Opening video device ....", flush=True )

import cv2
from PIL import Image
from PIL import ImageTk

cap = cv2.VideoCapture(0)
print( "Done...", flush=True )

# -- video open

from guizero import * 

app = App( width=720, height=665 )

title_box = Box(app, width="fill", align="top", border=True)
title = Text(title_box, text="HANSEI ADS CAR")

options_box = Box(app, height="fill", align="right", border=True)
options = Text(options_box, text="options")

content_box = Box(app, align="top", width="fill", height="fill", border=True)
pic_box = Box(content_box, width="fill", height="fill", border=True)
pic = None

if cap.isOpened() :
    ret, frame = cap.read()
    if ret :
        frame = cv2.flip(frame,0)
        height, width, channels = frame.shape 
        imgtk = ImageTk.PhotoImage(image=Image.fromarray( frame ))
        pic = Picture(pic_box, image=imgtk, width=width, height=height ) 
    pass
pass

if not pic :
    pic = Picture(pic_box, image="std1.gif" ) 
pass

#box = Box(content_box, width="fill", border=True)
control_box = Box(content_box, layout="grid", border=True)

font="Verdana 22 bold"

btn = Text(control_box, grid=[0,0], text="  " )
btn = PushButton(control_box, grid=[1,0], text=" ↑ ", command=car.forward )
btn.font = font
btn = Text(control_box, grid=[2,0], text="  " )

btn = PushButton(control_box, grid=[0,1], text="←", command=car.left  )
btn.font = font
btn = PushButton(control_box, grid=[1,1], text=" * ", command=car.stop  )
btn.font = font
btn = PushButton(control_box, grid=[2,1], text="→", command=car.right  )
btn.font = font

btn = Text(control_box, grid=[0,2], text="  " )
btn = PushButton(control_box, grid=[1,2], text=" ↓ ", command=car.backward  )
btn.font = font
btn = Text(control_box, grid=[2,2], text="  " )

buttons_box = Box(app, width="fill", align="bottom", border=True)
status = Text(buttons_box, text="status", align="left")

is_updating = 0
def update_pic() :
    #print( "Update pic" ) 
    global is_updating

    if cap.isOpened() :
        ret, frame = cap.read()
        if is_updating :
            pass
        elif ret :
            is_updating = 1
            frame = cv2.flip(frame,0)
            height, width, channels = frame.shape 
            pic.width = width
            pic.height = height
            img = Image.fromarray( frame )
            imgtk = ImageTk.PhotoImage(image=img)
            pic.image = imgtk
            is_updating = 0
        pass
    pass

    pic.after( 66, update_pic ) 
pass

import threading

# 1000 mili sec 후에 시간을 업데이트 한다.
pic.repeat( 2000, update_pic ) 

app.display()

# Release everything if job is finished
cap.release()

print( "Good bye...." )

pass
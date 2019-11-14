# coding: utf-8
from guizero import *

#picture1 = Picture(app, image="std1.gif", grid=[0,0] )

app = App()

title_box = Box(app, width="fill", align="top", border=True)
title = Text(title_box, text="HANSEI ADS CAR")

options_box = Box(app, height="fill", align="right", border=True)
options = Text(options_box, text="options")

content_box = Box(app, align="top", width="fill", height="fill", border=True)
pic_box = Box(content_box, width="fill", height="fill", border=True)
picture = Picture(pic_box, image="std1.gif" ) 

#box = Box(content_box, width="fill", border=True)
control_box = Box(content_box, layout="grid", border=True)

font="Verdana 22 bold"

btn = Text(control_box, grid=[0,0], text="  " )
btn = PushButton(control_box, grid=[1,0], text=" ↑ " )
btn.font = font
btn = Text(control_box, grid=[2,0], text="  " )

btn = PushButton(control_box, grid=[0,1], text="←" )
btn.font = font
btn = PushButton(control_box, grid=[1,1], text=" * " )
btn.font = font
btn = PushButton(control_box, grid=[2,1], text="→" )
btn.font = font

btn = Text(control_box, grid=[0,2], text="  " )
btn = PushButton(control_box, grid=[1,2], text=" ↓ " )
btn.font = font
btn = Text(control_box, grid=[2,2], text="  " )

buttons_box = Box(app, width="fill", align="bottom", border=True)
status = Text(buttons_box, text="status", align="left")

app.display()

print( "Hello...." )

pass
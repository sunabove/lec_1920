# coding: utf-8
from guizero import *

#picture1 = Picture(app, image="std1.gif", grid=[0,0] )

app = App()

title_box = Box(app, width="fill", align="top", border=True)
title = Text(title_box, text="HANSEI ADS CAR")

options_box = Box(app, height="fill", align="right", border=True)
options = Text(options_box, text="options")

content_box = Box(app, align="top", width="fill", height="fill", border=True)
Text(content_box, text="content", height="fill")

box = Box(content_box, width="fill", height="fill", align="center", border=True)
form_box = Box(box, layout="grid", align="center", border=True)

font="Verdana 19 bold"

btn = PushButton(form_box, grid=[0,0], text="  ", align="center" )
btn.font = font
btn = PushButton(form_box, grid=[1,0], text="↑", align="center" )
btn.font = font
btn = PushButton(form_box, grid=[2,0], text="  ", align="center" )
btn.font = font

btn = PushButton(form_box, grid=[0,1], text="←", align="center")
btn.font = font
btn = PushButton(form_box, grid=[1,1], text="*", align="center")
btn = PushButton(form_box, grid=[2,1], text="→", align="center")
btn.font = font

btn = PushButton(form_box, grid=[0,2], text="  ", align="center")
btn.font = font
btn = PushButton(form_box, grid=[1,2], text="↓", align="center")
btn.font = font
btn = PushButton(form_box, grid=[2,2], text="  ", align="center")
btn.font = font

buttons_box = Box(app, width="fill", align="bottom", border=True)
status = Text(buttons_box, text="status", align="left")

app.display()

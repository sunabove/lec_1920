# coding: utf-8
from guizero import App, ListBox, PushButton
app = App()
list_box = ListBox(app, items=["a list", "of items", "yay"], height="fill", align="left")
button = PushButton(app, width="fill", height="fill", align="right")
app.display()

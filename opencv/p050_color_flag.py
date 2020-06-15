# coding: utf-8

import cv2

flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
for idx, f in enumerate( flags ) :
    print( "[%d] %s:" % (idx, f) )
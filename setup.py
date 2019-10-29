# coding: utf-8
#!/usr/bin/env python

from setuptools import setup

setup(
   name='HANSEI ADS',
   version='1.0',
   description='HANSEI ADS',
   author='sunabove',
   author_email='sbmoon@nate.com',   
   packages=[ ],  #same as name
   #external packages as dependencies
   install_requires=['picamera', 'guizero', 'gpiozero', 'RPi.GPIO'], 
)
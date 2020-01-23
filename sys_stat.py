#!/usr/bin/python3
# coding: utf-8

def check_pkg( pkg ) : 
	try:
		import importlib
		importlib.import_module( pkg )
	except ModuleNotFoundError :
		print( '%s is not installed, installing it now!' % pkg )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg ] )
	pass
pass

for pkg in [ "RPi.GPIO", "gpiozero", "psutil", "netifaces" ] :
	check_pkg( pkg )
pass

# get ip address of devi
def get_ip( dev ) :
	ip = None 

	try : 
		import netifaces as ni 	
		ip = ni.ifaddresses( dev )[ni.AF_INET][0]['addr']

		print( "%s = %s" % ( dev, ip ) )
		
		if ip is not None :
			ip = ip.strip()
		pass
	except:
		pass
	pass

	return ip
pass

# check network interface
def check_interface(interface):
	import psutil
	import socket
	interface_addrs = psutil.net_if_addrs().get(interface) or []
	v = socket.AF_INET in [snicaddr.family for snicaddr in interface_addrs]

	print( "%s = %s" % ( interface, v ) )

	return v
pass

def ping( host ) : 
	import os
	hostname = "google.com" #example
	response = os.system("ping -c 1 " + hostname)

	#and then check the response...
	if response == 0:
		print( "success: %s" % host)
	else:
		print( "fail : %s" % host )
	pass

	return response is 0
pass

from gpiozero import LED
from time import sleep

led = LED(26)

led.off()

def blink_led( count = 1 ) :	
	interval = 0.2
	for _ in range( count ) : 
		print("+", end = '', flush=True )
		led.on()
		sleep( interval )
		print("\b-", end = '', flush=True)
		led.off()
		sleep( interval )
		print("\b", end = '', flush=True)
	pass
pass

print( "Press Ctrl + C to quit! ")

while True:
	print( "" )
	ip_eth0 = check_interface( "eth0" )
	ip_wlan0 = check_interface( "wlan0" )

	count = 1

	if ip_wlan0 :
		count += 1
	pass

	if ip_eth0 :
		count += 1
	pass

	if ping( "google.com" ) :
		count += 3
	pass

	blink_led( count )

	sleep( 2 )
pass


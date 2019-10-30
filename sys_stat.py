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

for pkg in [ "gpiozero", "netifaces" ] :
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

from gpiozero import LED
from time import sleep

led = LED(26)

print( "Press Ctrl + C to quit! ")

while True:
	print( "" )
	ip_eth0 = get_ip( "eth0" )
	ip_wlan0 = get_ip( "wlan0" )

	intervals = [ 1, 0 ] 

	if not ip_eth0 and not ip_wlan0 :
		intervals = [ 0.25, 0.25 ]
	elif not ip_eth0 and ip_wlan0 :
		intervals = [ 1, 1 ]
	elif ip_eth0 and ip_wlan0 :
		intervals = [ 1, 0 ]
	pass

	for idx, val in enumerate( intervals ):
		if 0 is idx%2 :
			print("+", end = '', flush=True )
			led.on()
			sleep( val )
		elif val is not 0 :
			print("\b-", end = '', flush=True)
			led.off()
			sleep( val )
		pass
		
		sleep( 1 )
		print("\b", end = '', flush=True)
	pass

	pass
pass


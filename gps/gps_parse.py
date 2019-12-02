# coding: utf-8
def check_pkg( pkg ) : 
	try:
		import importlib
		mode_name = pkg.split(",")[0].strip() 
		importlib.import_module( mode_name )
	except ModuleNotFoundError :
		print( '%s is not installed, installing it now!' % mode_name )
		import sys 
		try:
			from pip import main as pipmain
		except:
			from pip._internal import main as pipmain
		pass
		pipmain( ['install', pkg.split(",")[-1].strip() ] )
	pass
pass

for pkg in [ "serial, pyserial", "pynmea2" ] :
	check_pkg( pkg )
pass



import serial
import pynmea2

gps_parse_cnt = 0 
def parseGPS(str):
    if 'GGA' in str :
        global gps_parse_cnt
        gps_parse_cnt += 1
        msg = pynmea2.parse(str)
        #print( "[%04d] %s" % ( gps_parse_cnt, str ) , end ="" )
        print( "[%04d] Time: %s Lat: %s %s Lon: %s %s Altitude: %s %s Satellites: %s" % ( gps_parse_cnt, msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats) )
    pass
pass 

def read_gps() :
    while 1 :  
        try : 
            gps_serial = serial.Serial("/dev/serial0", baudrate = 9600, timeout = 20 )
            while 1 :
                str = gps_serial.readline()
                parseGPS(str.decode( "utf-8"))
            pass
        except Exception as e:
            #print( str(e) )
            #print( "Serial Device Error" )
            import time
            time.sleep( 3 )
            pass
        pass
    pass
pass

if __name__ == "__main__" : 
    read_gps()
pass
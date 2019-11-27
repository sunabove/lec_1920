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

for pkg in [ "serial, pyserial" ] :
	check_pkg( pkg )
pass

def parseGPS(data): #    print "raw:", data #prints raw data
    if data[0:6] in ( "$GPRMC", "$GNRMC" ) :
        sdata = data.split(",")
        if sdata[2] == 'V':
            print( "no satellite data available" )
            return
        print( "---Parsing GPRMC---" )
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
 
        print( "time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s" % (time,lat,dirLat,lon,dirLon,speed,trCourse,date) )
    pass
pass
 
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"
 
 
print( "Receiving GPS data" )
import serial
ser = serial.Serial( "/dev/serial0", baudrate = 9600, timeout = 0.5)
count = 1
while 1 :
   data = ser.readline()
   print( "[%04d] %s" % ( count, data ) )
   count += 1
   parseGPS(data)
pass
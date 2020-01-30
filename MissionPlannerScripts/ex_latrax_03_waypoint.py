import sys
import math
import clr
import time
import System
from System import Byte

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink

idmavcmd = MAVLink.MAV_CMD.WAYPOINT
id = int(idmavcmd)

alt = 0 

home = Locationwp().Set( 37.308896,	127.000060, alt, id)

to = Locationwp()
Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
Locationwp.p1.SetValue(to, 15)
Locationwp.alt.SetValue(to, alt)

wp1 = Locationwp().Set(37.30892020,	126.99997100, alt, id)
wp2 = Locationwp().Set(37.30887110,	126.99937280, alt, id)
wp3 = Locationwp().Set(37.30844450,	126.99937280, alt, id)

print "set wp total"
MAV.setWPTotal(5)
print "upload home - reset on arm"
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
print "upload to"
MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
print "upload wp1"
MAV.setWP(wp1,2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
print "upload wp2"
MAV.setWP(wp2,3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
print "upload wp3"
MAV.setWP(wp3,4,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
print "final ack"
MAV.setWPACK()

print "done"
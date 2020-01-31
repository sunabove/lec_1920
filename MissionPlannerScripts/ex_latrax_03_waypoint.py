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

def speak( text ) :
    MissionPlanner.MainV2.speechEnable = True
    print text 
    MissionPlanner.MainV2.speechEngine.SpeakAsync( text )

    time.sleep( len(text)/5 + 1 )
pass

idmavcmd = MAVLink.MAV_CMD.WAYPOINT
id = int(idmavcmd)

alt = 0 

home = Locationwp().Set( 37.344628, 126.952841, alt, id)

to = Locationwp()
Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
Locationwp.p1.SetValue(to, 15)
Locationwp.alt.SetValue(to, alt)

points = []
points.append( (37.34464360, 126.95298940) )
points.append( (37.34470970, 126.95375250) )
points.append( (37.34481310, 126.95407300) )
points.append( (37.34544640, 126.95396970) )
points.append( (37.34588460, 126.95388530) )
points.append( (37.34634310, 126.95380080) )
points.append( (37.34641340, 126.95369210) )
points.append( (37.34641340, 126.95322010) )
points.append( (37.34642410, 126.95311680) )
points.append( (37.34656910, 126.95266220) )
points.append( (37.34653600, 126.95250790) )
points.append( (37.34647530, 126.95243950) )
points.append( (37.34638570, 126.95242350) )
points.append( (37.34478320, 126.95279490) )
points.append( (37.34467980, 126.95282040) )

speak( "set wp total" )
MAV.setWPTotal( 2 + len( points ) )

speak( "uploading way points ..." )
idx = 0 
MAV.setWP(home, idx,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
idx += 1 
MAV.setWP(to, idx,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
idx += 1

for p in points : 
    print "upload wp %d" % idx
    wp = Locationwp().Set( p[0], p[1], alt, id) 
    MAV.setWP(wp, idx, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT) 
    idx += 1
pass

speak( "final ack" )
MAV.setWPACK()

speak( "done uploading way points." )


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

speak( 'Start Script' )

Script.SendRC(3,1600,False)
Script.SendRC(8,1000,True)
speak(  'sent throttle down' )
MAV.doARM(True)
speak(  'sent arm' )
Script.SendRC(8,2000,True)
speak(  'sent throttle up' )
Script.ChangeMode("Guided")
speak(  'sent guided' )
MAV.doCommand(MAVLink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, 100)
speak(  'sent takeoff' )

speak( "throttle up")
Script.SendRC(3,1900,True) # throttle up

Script.Sleep(2000)  

speak( "throttle down")
Script.SendRC(3,1500,True) # throttle down

Script.Sleep(2000)  

speak( "Testing Done." )
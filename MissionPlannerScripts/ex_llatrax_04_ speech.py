import sys
import math
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class

def speak( text ) :
	MissionPlanner.MainV2.speechEnable = True
	print text 
	MissionPlanner.MainV2.speechEngine.SpeakAsync( text )
pass

speak( "Start Script" )

for i in range( 3 ) : 
	speak("test %d" % i )
	time.sleep(1)
pass

speak( "Good bye!")

pass
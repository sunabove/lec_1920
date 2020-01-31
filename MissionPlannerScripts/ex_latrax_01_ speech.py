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
	time.sleep( len(text)/5 + 1 )
pass

speak( "Start Script" )

for i in range( 3 ) : 	
	speak("test %d" % i ) 
pass

speak( "I am beautiful." )

speak( "Good bye!")

pass
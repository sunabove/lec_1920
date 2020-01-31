import sys
import clr
import time
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") 
time.sleep(10)                                             
# wait 10 seconds before starting
print 'Starting Mission'
Script.ChangeMode("Guided") 
print 'Guided Mode'
item = MissionPlanner.Utilities.Locationwp() # creating waypoint
alt = 0
lat = 37.344628
lng = 126.952841
MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat) 
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng) 
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt) 
print 'WP 1 set'
MAV.setGuidedModeWP(item)                                    # tells UAV "go to" the set lat/long @ alt
print 'Going to WP 1'
time.sleep(10)
# wait 10 seconds
print 'Ready for next WP'
lat = 37.34464360
lng = 126.95298940
MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)
print 'WP 2 set'
MAV.setGuidedModeWP(item)
print 'Going to WP 2'
time.sleep(10) 
print 'Mission Complete'

Script.ChangeMode("RTL")                                      # Return to Launch point
print 'Returning to Launch'
time.sleep(10)
Script.ChangeMode("LOITER")                                # switch to "LOITER" mode
print 'LOITERING'


# cs.???? = currentstate, any variable on the status tab in the planner can be used.
# Script = options are 
# Script.Sleep(ms)
# Script.ChangeParam(name,value)
# Script.GetParam(name)
# Script.ChangeMode(mode) - same as displayed in mode setup screen 'AUTO'
# Script.WaitFor(string,timeout)
# Script.SendRC(channel,pwm,sendnow)
# 

print 'Start Script'

for chan in range(1,9):
    Script.SendRC(chan,1500,False)
Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

Script.Sleep(5000)


Script.SendRC(3,1500,False)
Script.SendRC(4,1982,True)
cs.messages.Clear()
print 'ARMING MOTORS' 
Script.SendRC(4,1982,True)
Script.Sleep(5000)  
print 'Motors Armed!'

Script.SendRC(3,1900,True) # throttle

Script.Sleep(2000)  

Script.SendRC(3,1400,True) # throttle back to land

thro = 1350 # will decend 

Script.SendRC(3,1000,False)
Script.SendRC(4,1000,True)
Script.WaitFor('DISARMING MOTORS',30000)
Script.SendRC(4,1500,True)

print 'Mission complete'
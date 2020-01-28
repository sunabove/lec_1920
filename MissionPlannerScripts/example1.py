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
Script.SendRC(3,1550,True) # throttle

for chan in range(1,9):
    Script.SendRC(chan,1500,False)
Script.SendRC(3,Script.GetParam('RC3_MIN'),True)

Script.Sleep(5000)
while cs.lat == 0:
    print 'Waiting for GPS'
    Script.Sleep(1000)
pass

print 'Got GPS'
jo = 10 * 13
print jo
Script.SendRC(3,1000,False)
Script.SendRC(4,2000,True)
cs.messages.Clear()
Script.WaitFor('ARMING MOTORS',30000)
Script.SendRC(4,1500,True)
print 'Motors Armed!'

Script.SendRC(3,1700,True)

if 0 : 
    while cs.alt < 50:
        Script.Sleep(50)
    pass
pass

if 0: 
    Script.SendRC(5,2000,True) # acro

    Script.SendRC(1,2000,False) # roll
    Script.SendRC(3,1370,True) # throttle
pass

Script.SendRC(3,1500,True) # throttle

if 0 : 
    while cs.roll > -45: # top hald 0 - 180
        Script.Sleep(5)
    pass

    while cs.roll < -45: # -180 - -45
        Script.Sleep(5)
    pass
pass

Script.SendRC(5,1500,False) # stabalise
Script.SendRC(1,1500,True) # level roll
Script.Sleep(2000) # 2 sec to stabalise
Script.SendRC(3,1300,True) # throttle back to land

thro = 1350 # will decend

if 0 : 
    while cs.alt > 0.1:
        Script.Sleep(300)
    pass
pass

Script.SendRC(3,1000,False)
Script.SendRC(4,1000,True)
Script.WaitFor('DISARMING MOTORS',30000)
Script.SendRC(4,1500,True)

print 'Roll complete'
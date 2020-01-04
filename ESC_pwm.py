from gpiozero import PWMLED
from time import sleep

pwmESC = PWMLED(17)

for x in range( 10, 17 ) :
   pwmESC.value = x*0.01
   print( "pwm value = %5.2f" % pwmESC.value )
   sleep(0.7) 

pwmESC.value = 0
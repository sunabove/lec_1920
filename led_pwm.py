from gpiozero import PWMLED
from time import sleep

pwmLed = PWMLED(4)

while True:
   for x in range( 101 ) :
      pwmLed.value = x*0.01
      sleep(0.02)

   sleep( 0.3 )

   for x in range( 101 ) :
      pwmLed.value = (100 - x)*0.01
      sleep(0.02)

   sleep( 0.3 )
pass

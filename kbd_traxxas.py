# coding: utf-8
import curses
from gpiozero import Robot 
from gpiozero import PWMLED, Servo

class Car :
    pass

    def __init__( self )
        self.servo = Servo(4) 
        self.esc = PWMLED(17)

        self.pwm_min = 0.148
        self.pwm_max = 0.151
    pass

    def forward( self ) :
        esc = self.esc
        if self.pwm_min > esc.value
            esc.value = self.pwm_min
        else:
            esc.value = esc.value + 0.01
        pass
    pass

    def backward( self ) :
        pass
    pass

    def left( self ) :
        servo = self.servo
        servo.value = servo.value - 0.1
    pass

    def right( self ) :
        servo = self.servo
        servo.value = servo.value + 0.1
    pass

    def stop(self):
        self.servo.value = 0 
        self.esc.value = 0
    pass

pass

car = Car()

actions = {
    curses.KEY_UP:    car.forward,
    curses.KEY_DOWN:  car.backward,
    curses.KEY_LEFT:  car.left,
    curses.KEY_RIGHT: car.right,
}

def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            car.stop()
        pass
    pass
pass

if __name__ == "__main__":
    curses.wrapper(main)
pass

# end
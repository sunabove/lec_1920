# coding: utf-8
import curses
from gpiozero import PWMLED, Servo

class Car :

    # 초기화 
    def __init__( self ) :
        self.servo = Servo(4) 
        self.esc = PWMLED(17)

        self.pwm_min = 0.148
        self.pwm_max = 0.151

        self.esc.value = 0.0
        self.servo.value = 0.0
    pass

    # 전진
    def forward( self ) :
        esc = self.esc

        value = esc.value + 0.01

        if self.pwm_min > value :
            value = self.pwm_min
        elif self.pwm_max < value :
            value = self.pwm_max
        pass

        esc.value = value
    pass

    # 후진 
    def backward( self ) :
        esc = self.esc

        value = esc.value - 0.01

        if 0 > value :
            value = 0 
        elif self.pwm_max < value :
            value = self.pwm_max
        pass

        esc.value = value
    pass

    # 좌회전 
    def left( self ) :
        servo = self.servo
        value = servo.value + 0.1

        if 1.0 < value :
            value = 1.0
        elif -1.0 > value :
            value = -1.0
        pass
        
        servo.value = value
    pass

    # 우회전 
    def right( self ) :
        servo = self.servo
        value = servo.value - 0.1

        if 1.0 < value :
            value = 1.0
        elif -1.0 > value :
            value = -1.0
        pass
        
        servo.value = value
    pass

    # 정지 
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

def car_control(window):
    next_key = None
    while 1:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        pass

        if key != -1:
            # KEY PRESSED
            curses.halfdelay(1)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            pass
        pass
    pass
pass

if __name__ == "__main__":
    curses.wrapper(car_control)
pass

# end
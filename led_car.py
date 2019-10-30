# coding: utf-8
import curses
from gpiozero import Robot, LED

class Car( Robot ) :

    def __init__(self, left, right, *, pwm=True, pin_factory=None):
        print("A car is ready.")
        super().__init__( left, right, pwm, pin_factory )

        self.fw_led = LED( 27 )
    pass

    def forward(self, speed=1):
        super().forward(speed)
        self.fw_led.on()
    pass

    def backward(self, speed=1):
        super().backward(speed)
        self.fw_led.off()
    pass

    def left(self, speed=1):
        super().left( speed )
        self.fw_led.off()
    pass

    def right(self, speed=1):
        super().right( speed )
        self.fw_led.off()
    pass

    def reverse(self):
        super().reverse()
        self.fw_led.off()
    pass

    def stop(self):
        super().stop()
        self.fw_led.off()
    pass

pass

car = Car(left=(22, 23), right=(9, 25))

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

if __name__ == '__main__':
    curses.wrapper(main)
pass

# end
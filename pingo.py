import machine
import time

PIN = 12
FREQUENCY = 50  # Hz

# common duty cyles
# somewhere between 0 and 1023
LEFT = 25
RIGHT = 124
CENTER = 77


class Servo:
    def __init__(self, pin, freq, dc_defaults):
        """Create servo connected with frequency freq to pin. dc_defaults
        contains default duty cylces for values of left, right and
        center.
        """

        pin = machine.Pin(pin)
        self.pwm = machine.PWM(pin, freq=FREQUENCY)
        self.left, self.right, self.center = dc_defaults

    def left_right_center(self):
        print("turn left")
        self.pwm.duty(self.left)
        time.sleep(1)

        print("turn right")
        self.pwm.duty(self.right)
        time.sleep(1)

        print("center")
        self.pwm.duty(self.center)

    def left_to_right(self):
        stepsize = int((self.right - self.left) / 10)

        for dc in range(self.left, self.right+1, stepsize):
            print("dc", dc)
            self.pwm.duty(dc)
            time.sleep(0.5)


def main():
    print("starting pingo on pin", PIN, "with", FREQUENCY, "Hz")
    servo = Servo(pin=PIN, freq=FREQUENCY, dc_defaults=[LEFT, RIGHT, CENTER])
    servo.left_right_center()
    #servo.left_to_right()


if __name__ == "__main__":
    main()

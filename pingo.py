import machine
import network
import time

# configure the servo
SERVOPIN = 12
FREQUENCY = 50  # Hz

# common duty cyles
# somewhere between 0 and 1023
LEFT = 25
RIGHT = 124
CENTER = 77

# configure network access
SSID = "PectroNet Gastzugang"
PASS = "123456543212"


class WifiClient:
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd

        # Create a station interface
        self.sta_if = network.WLAN(network.STA_IF)
        # activate the interface
        self.sta_if.active(True)

    def connect(self):
        # and connect
        print("connecting to", self.ssid)
        self.sta_if.connect(self.ssid, self.passwd)
        print("waiting some seconds")
        time.sleep(5)
        print("connected", self.sta_if.isconnected())
        print("IP", self.sta_if.ifconfig())


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


def deepsleep():
    """Go into deep sleep mode. GPIO16 (D0) must be connected to RST
    (RST)."""

    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEP_SLEEP)
    # set alarm time (in ms)
    rtc.alarm(rtc.ALARM0, 10000)
    # sleep
    machine.deepsleep()


def main():
    print("connecting to wifi")
    wifi = WifiClient(ssid=SSID, passwd=PASS)
    wifi.connect()

    print("starting servo on pin", SERVOPIN, "with", FREQUENCY, "Hz")
    servo = Servo(pin=SERVOPIN, freq=FREQUENCY,
                  dc_defaults=[LEFT, RIGHT, CENTER])
    servo.left_right_center()
    # servo.left_to_right()

    
    # go into sleep mode
    #deepsleep()


if __name__ == "__main__":
    main()

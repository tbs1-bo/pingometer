import machine
import network
import time
import usocket
from umqtt.simple import MQTTClient

# configure the servo
SERVOPIN = 12  # GPIO12 (D6)
FREQUENCY = 50  # Hz

# how many ms to sleep in deep sleep mode
DEEPSLEEP_TIME = 20000

# common duty cyles
# somewhere between 0 and 1023
LEFT = 25
RIGHT = 124
CENTER = 77

# configure network access
SSID = "MyNetwork"
PASS = "MyPassword"

# Location for data value that should be retrieved
DATA_URL = "http://www.bakera.de/data.txt"


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
        if not self.sta_if.isconnected():
            print("connecting to", self.ssid)
            self.sta_if.connect(self.ssid, self.passwd)

            # waiting till connected
            while not self.sta_if.isconnected():
                pass

        print("connected", self.sta_if.isconnected())
        print("IP", self.sta_if.ifconfig())

    def is_reachable(self, ip, port):
        socket = usocket.socket()
        try:
            socket.connect((ip, port))
            return True
        except:
            return False


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

    def subscribe_callback(self, msg, _topic):
        """Calback method for a topic. Value in msg will be interpreted as
        integer percent value between 0 and 100."""

        val_percent = int(msg)
        # convert percent value in values between 0 and 1023
        dc = val_percent * 1023 / 100
        self.pwm.duty(int(dc))


def deepsleep():
    """Go into deep sleep mode. GPIO16 (D0) must be connected to RST
    (RST)."""

    # wait some time before going into deesleep mode - otherwise no
    # intervention possible when problems occur.
    time.sleep(5000)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set alarm time (in ms)
    rtc.alarm(rtc.ALARM0, DEEPSLEEP_TIME)
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

    # fetch value from broker
    mqtt = MQTTClient("zeigometer", MQTT_HOST)
    mqtt.set_callback(servo.subscribe_callback)
    mqtt.connect()
    mqtt.subscribe(MQTT_TOPIC)
    # wait for msg - non-blocking
    mqtt.chk_msg()
    time.sleep(MQTT_WAIT_TIME)
    mqtt.disconnect()

    # checking reachability
    if wifi.is_reachable(IP, PORT):
        print(IP, "reachable")
    else:
        print(IP, "unreachable")

    # go into sleep mode
    #deepsleep()


if __name__ == "__main__":
    main()

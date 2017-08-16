import machine
import network
import time
import socket
import credentials

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

    def diconnect(self):
        self.sta_if.disconnect()


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

        print("msg received", msg, _topic)
        val_percent = int(msg)
        # convert percent value in values between 0 and 1023
        dc = val_percent * 1023 / 100
        print("change dc to", int(dc))
        self.pwm.duty(int(dc))


def http_get_value(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host),
                 'utf8'))
    while True:
        data = s.recv(100)

        if b"\r\n\r\n" in data:
            # the last 100 Bytes should contain the payload
            val = data.split(b"\r\n\r\n")[-1]
            print("converting", val)
            val = int(val.strip())
            s.close()
            return val

    s.close()


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


def callback(msg, topic):
    print("received", msg, topic)


def main():
    print("connecting to wifi")
    wifi = WifiClient(ssid=credentials.SSID, passwd=credentials.PASS)
    wifi.connect()

    """print("starting servo on pin", SERVOPIN, "with", FREQUENCY, "Hz")
    servo = Servo(pin=SERVOPIN, freq=FREQUENCY,
                  dc_defaults=[LEFT, RIGHT, CENTER])
    servo.left_right_center()
    # servo.left_to_right()"""

    val = http_get_value(DATA_URL)
    if val is not None:
        print("Got value", val)

    wifi.disconnect()
    # go into sleep mode
    #deepsleep()


if __name__ == "__main__":
    main()

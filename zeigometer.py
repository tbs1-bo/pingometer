import machine
import network
import time
import socket
import config


class WifiClient:
    def __init__(self, ssid, passwd):
        self.ssid = ssid
        self.passwd = passwd

        # Create and activate station interface
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)

    def connect(self):
        if not self.sta_if.isconnected():
            print("connecting to", self.ssid)
            self.sta_if.connect(self.ssid, self.passwd)

            # waiting until connected
            while not self.sta_if.isconnected():
                pass

        print("connected with IP", self.sta_if.ifconfig())

    def disconnect(self):
        self.sta_if.disconnect()

    def http_get_value(self, url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host),
                     'utf8'))

        # two new lines separate the header from the payload
        header_payload_separator = b'\r\n\r\n'
        while True:
            data = s.recv(100)

            if header_payload_separator in data:
                # the last 100 Bytes should contain the payload
                val = data.split(header_payload_separator)[-1]
                print("converting", val)
                val = int(val.strip())
                s.close()
                return val

        s.close()


class Servo:
    def __init__(self, pin, freq, dc_left, dc_right):
        """Create servo connected with frequency freq to pin. dc_defaults
        contains default duty cylces for values of left and right.
        """

        pin = machine.Pin(pin)
        self.pwm = machine.PWM(pin, freq=freq)
        self.left, self.right = dc_left, dc_right

    def left_right_center(self):
        print("turn left")
        self.change_needle(0)
        time.sleep(1)

        print("turn right")
        self.change_needle(100)
        time.sleep(1)

        print("center")
        self.change_needle(100)
        time.sleep(1)

    def left_to_right(self):
        for rightiness in range(100):
            self.change_needle(rightiness)
            time.sleep(0.5)

    def change_needle(self, rightiness):
        """Change the position of the needle from 0 (left) to 100 (right)."""

        if not 0 <= rightiness <= 100:
            print("ignoring wrong value range")
            return
        
        delta_lr = self.right - self.left
        dc = self.left + delta_lr * rightiness / 100
        print("change dc to", int(dc))
        self.pwm.duty(int(dc))


def deepsleep():
    """Go into deep sleep mode. GPIO16 (D0) must be connected to RST
    (RST)."""

    # wait some time before going into deesleep mode - otherwise no
    # intervention possible when problems occur.
    time.sleep(5)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set alarm time (in ms)
    print("setting alarm", config.DEEPSLEEP_TIME)
    rtc.alarm(rtc.ALARM0, config.DEEPSLEEP_TIME)
    # sleep
    print("starting deep sleep...")
    machine.deepsleep()


def callback(msg, topic):
    print("received", msg, topic)


def main():
    print("connecting to wifi")
    wifi = WifiClient(ssid=config.SSID, passwd=config.PASS)
    wifi.connect()

    print("starting servo on pin", config.SERVOPIN, "with",
          config.FREQUENCY, "Hz")
    servo = Servo(pin=config.SERVOPIN, freq=config.FREQUENCY,
                  dc_left=config.LEFT, dc_right=config.RIGHT)
    # servo.left_right_center()
    # servo.left_to_right()

    try:
        val = wifi.http_get_value(config.DATA_URL)
        if val is not None:
            print("Got value", val)
            servo.change_needle(val)
    except Exception as ex:
        print("Error occured", ex)

    print("disconnecting from WiFi")
    wifi.disconnect()

    # go into sleep mode
    print("going into deep sleep mode")
    deepsleep()


if __name__ == "__main__":
    main()

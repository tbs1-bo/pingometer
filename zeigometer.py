import machine
import network
import time
import socket
import config


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

    def disconnect(self):
        self.sta_if.disconnect()

    def http_get_value(self, url):
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host),
                     'utf8'))

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
    def __init__(self, pin, freq, dc_defaults):
        """Create servo connected with frequency freq to pin. dc_defaults
        contains default duty cylces for values of left, right and
        center.
        """

        pin = machine.Pin(pin)
        self.pwm = machine.PWM(pin, freq=freq)
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
        time.sleep(1)

    def left_to_right(self):
        stepsize = int((self.right - self.left) / 10)

        for dc in range(self.left, self.right+1, stepsize):
            print("dc", dc)
            self.pwm.duty(dc)
            time.sleep(0.5)

    def change_needle(self, perc_right):
        """Change the position of the needle from 0 (left) to 100 (right)."""

        if not 0 <= perc_right <= 100:
            print("wrong value range")
            return
        
        delta_lr = self.right - self.left
        dc = self.left + delta_lr * perc_right / 100
        print("change dc to", int(dc))
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
    rtc.alarm(rtc.ALARM0, config.DEEPSLEEP_TIME)
    # sleep
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
                  dc_defaults=[config.LEFT, config.RIGHT, config.CENTER])
    servo.left_right_center()
    # servo.left_to_right()

    val = wifi.http_get_value(config.DATA_URL)
    if val is not None:
        print("Got value", val)
        servo.change_needle(val)

    print("disconnecting from WiFi")
    wifi.disconnect()

    # go into sleep mode
    #print("going into deep sleep mode")
    #deepsleep()


if __name__ == "__main__":
    main()

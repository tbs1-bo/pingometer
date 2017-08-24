import machine
import network
import time
import socket
import config
import umqtt.simple


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


class ServoController:
    def __init__(self, host, topic, servo, keepalive=5, qos=1):
        self.topic = topic
        self.host = host
        self.servo = servo
        self.keepalive = keepalive
        self.qos = qos

    def loop_forever(self):
        mqtt = umqtt.simple.MQTTClient('esp123', self.host,
                                       keepalive=self.keepalive)
        mqtt.set_callback(lambda _topic, value:
                          self._change_needle(value))
        print("connecting to MQTT Broker")
        mqtt.connect()
        print("Subscribing to topic", self.topic)
        mqtt.subscribe(self.topic, self.qos)
        print("Awaiting messages from Broker")
        while True:
            mqtt.wait_msg()

    def _change_needle(self, val):
        try:
            newval = int(val)
            self.servo.change_needle(newval)
        except Exception as ex:
            print("Exception occured", ex)


def deepsleep():
    """Go into deep sleep mode. GPIO16 (D0) must be connected to RST
    (RST)."""

    # wait some time before going into deesleep mode - otherwise no
    # intervention possible when problems occur.
    time.sleep(5)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set alarm time (in ms)
    print("setting alarm for RTC", config.DEEPSLEEP_TIME)
    rtc.alarm(rtc.ALARM0, config.DEEPSLEEP_TIME)
    # sleep
    print("starting deep sleep...")
    machine.deepsleep()


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

    # start timer
    tim = machine.Timer(0)
    print("Timer for deepsleep will elapse in (ms)", config.MAX_UPTIME)
    tim = tim.init(period=config.MAX_UPTIME,
                   mode=machine.Timer.ONE_SHOT,
                   callback=lambda _timer: deepsleep())

    print("Creating servo controller")
    servo_con = ServoController(config.MQTT_HOST, config.MQTT_TOPIC, servo)
    servo_con.loop_forever()


if __name__ == "__main__":
    main()

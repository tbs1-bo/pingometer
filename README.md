Zeigometer
==========

A servo is connected to an ESP8266, reads analog values from an MQTT
Broker and sends them to a servo that visualizes these values on a
scale. The project is mainly inspired by the
[pingo meter project](https://www.raspberrypi.org/magpi/pingometer/)
from the Raspberry Pi Magazine.


Sketch
------

![sketch](doc/sketch_breadboard.png)

- The servo is connected to the VCC and Ground for power supply.
- GPIO12 is used as PWM pin for controlling the servo.
- GPIO16 and REST are connected to awake the ESP8266 from deep sleep
  mode.


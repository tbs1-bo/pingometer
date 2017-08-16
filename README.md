Zeigometer
==========

![zeigometer](doc/zeigometer.jpg)

A servo is connected to an ESP8266, reads analog values from a web ressource.
sends the value to a servo that visualizes these value on a
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

Configuration
-------------

Move `config_sample.py` to `config.py` and set the correct values.

Making
------

Some images during the making of the project.

![esp connected](doc/esp_connected.jpg)

![servo glued](doc/servo_glued.jpg)

![servo on front hole](doc/servor_front_hole.jpg)


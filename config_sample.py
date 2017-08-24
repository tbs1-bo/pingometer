# Copy this file to config.py and update the values below.
#

# Network settings to connect the device to.
SSID = "My Network"
PASS = "My Password"

# configure the servo motor
SERVOPIN = 12  # GPIO12 (D6)
FREQUENCY = 50  # Hz

# MQTT host and topic where the value of the needle might come from
MQTT_HOST = 'iot.eclipse.org'
MQTT_TOPIC = 'zeigometer/value'

# maximum runtime (in ms) of the chip before going into deepsleep
MAX_UPTIME = 20000

# how many ms to sleep in deep sleep mode after that amount of time,
# the ESP8266 awakes again. For this to work, pin GPIO16 hat to be
# connected with the RESET Pin.
DEEPSLEEP_TIME = 20000

# common duty cyles that must range from 0 to 1023 and should conform
# to positions of the needle.
LEFT = 25
RIGHT = 125

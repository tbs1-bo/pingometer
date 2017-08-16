# Copy this file to config.py and update the values below.
#

# Network settings to connect the device to.
SSID = "My Network"
PASS = "My Password"

# configure the servo motor
SERVOPIN = 12  # GPIO12 (D6)
FREQUENCY = 50  # Hz

# Location for data value that should be retrieved. It has to contain
# only one interger value ranging from 0 to 100.
DATA_URL = "http://www.example.com/data.txt"

# how many ms to sleep in deep sleep mode after that amount of time,
# the ESP8266 awakes again. For this to work, pin GPIO16 hat to be
# connected with the RESET Pin.
DEEPSLEEP_TIME = 20000

# common duty cyles that must range from 0 to 1023 and should conform
# to positions of the needle.
LEFT = 25
RIGHT = 125


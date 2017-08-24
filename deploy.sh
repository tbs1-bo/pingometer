#!/bin/sh

AMPY_PORT=/dev/ttyUSB0


# move onto the device with ampy
#
echo "Putting main files onto the device"
ampy put zeigometer.py
ampy put boot.py

# MQTT libs
LS=$(ampy ls)
if ! echo $LS | grep --quiet 'umqtt'; then
    echo "Putting MQTT libs onto the device"

    ampy mkdir umqtt;
    ampy put umqtt/simple.py umqtt/simple.py;
    ampy put umqtt/robust.py umqtt/robust.py;
fi

echo "Files and directories on the device:"
ampy ls

import network

SSID = "PectroNet Gastzugang"
PASS = "123456543212"


def main():
    # Create a station interface
    sta_if = network.WLAN(network.STA_IF)
    # activate the interface
    sta_if.active(True)
    # and connect
    print("connecting to", SSID)
    sta_if.connect(SSID, PASS)
    print("connected", sta_if.isconnected())
    print("IP", sta_if.ifconfig())

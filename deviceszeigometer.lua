-- This module shows the number of clients that try to
-- probe the ESP8266 in AP-mode.

-- Look for devices nearby and show them on the zeigometer.
-- from
-- https://nodemcu.readthedocs.io/en/master/en/modules/wifi/#wifieventmonregister

require "credentials"

conf = {}
conf.mqtt = {}
conf.mqtt.host = "iot.eclipse.org"
conf.mqtt.port = 1883
conf.mqtt.topic = "zeigometer"

clients = {}

function probe_received_cb(T)
   -- print("\n\tAP - PROBE REQUEST RECEIVED".."\n\tMAC: ".. T.MAC.."\n\tRSSI: "..T.RSSI)

   -- check if client already seen
   if clients[T.MAC] then
      clients[T.MAC] = clients[T.MAC] + 1
   else
      clients[T.MAC] = 1
   end

   count = 0
   for k,v in pairs(clients) do
      count = count + 1
      print("key:"..k.." val:"..v)
      mqtt_client:publish(conf.mqtt.topic..'/probe/'..k, v, 1, 1)
   end
   print("#probes: "..count)
   --                                          qos retain
   mqtt_client:publish(conf.mqtt.topic..'/numprobes', count, 1, 1)
end

function got_ip_cb()
   print("connected to wifi with:"..wifi.sta.getip())
   mqtt_client = mqtt.Client("zeigometer", 100)
   mqtt_client:connect(conf.mqtt.host, conf.mqtt.port, 0,
		       -- callback when connected
		       mqtt_connected_cb)
end

function mqtt_connected_cb()
   print("connected to mqtt broker")
   wifi.eventmon.register(wifi.eventmon.AP_PROBEREQRECVED,
			  probe_received_cb)
end

-- configure station and start connection
sta_config={}
sta_config.ssid = WIFI_SSID
sta_config.pwd = WIFI_PASSWORD
sta_config.got_ip_cb = got_ip_cb

wifi.sta.config(sta_config)

-- require "deviceszeigometer"
-- dofile("deviceszeigometer.lua")

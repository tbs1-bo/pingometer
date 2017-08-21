-- This module shows the number of clients that try to
-- probe the ESP8266 in AP-mode.

-- Look for devices nearby and show them on the zeigometer.
-- from
-- https://nodemcu.readthedocs.io/en/master/en/modules/wifi/#wifieventmonregister

require "credentials"

conf = {}
conf.mqtt = {
   host = "iot.eclipse.org",
   port = 1883,
   topic = "zeigometer"
}

clients = {}

function probe_received_cb(T)
   -- print("\n\tAP - PROBE REQUEST RECEIVED".."\n\tMAC: ".. T.MAC.."\n\tRSSI: "..T.RSSI)

   -- check if client already seen
   if clients[T.MAC] == nil then
      clients[T.MAC] = {}
      clients[T.MAC].count = 0
   end

   clients[T.MAC].count = clients[T.MAC].count + 1
   clients[T.MAC].rssi = T.RSSI

   count = 0
   for mac,vars in pairs(clients) do
      count = count + 1
      print("mac:"..mac.." count:"..vars.count.." rssi:"..vars.rssi)
      mqtt_client:publish(conf.mqtt.topic..'/probe/'..mac.."/count",
			  vars.count, 1, 1)
      mqtt_client:publish(conf.mqtt.topic..'/probe/'..mac.."/rssi",
			  vars.rssi, 1, 1)
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

function time_elapsed_cb()
   print("time over")
   -- TODO enter deep sleep mode
   -- https://nodemcu.readthedocs.io/en/master/en/modules/node/#nodedsleep
end

-- configure station and start connection
sta_config={}
sta_config.ssid = WIFI_SSID
sta_config.pwd = WIFI_PASSWORD
sta_config.got_ip_cb = got_ip_cb

local timer = tmr.create()
timer:register(10000, tmr.ALARM_SINGLE, time_elapsed_cb)
timer:start()

wifi.sta.config(sta_config)

-- require "deviceszeigometer"
-- dofile("deviceszeigometer.lua")

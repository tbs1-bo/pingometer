# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import gc
import zeigometer

import time

print("started")

# some rescue time we will wait before something happens.
# comment out if sure that everything works fine.
#
time.sleep(5)

gc.collect()
zeigometer.main()

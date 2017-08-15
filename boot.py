# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import connect
import gc
import pingo

gc.collect()
connect.main()
pingo.main()

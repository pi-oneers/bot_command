#! /usr/bin/env python

import time
import pibot

bot = pibot.PiBot()
   
while True:

    print "Distance is", bot.getUltrasonicDistance()
    time.sleep( 0.1 )
        
#! /usr/bin/env python

import time
import pibot
import sys

bot = pibot.PiBot()
speed = 255

if len( sys.argv ) > 1:
    speed = int( sys.argv[ 1 ] )
   
while True:

    # Drive forwards
    bot.setMotorSpeeds( speed, speed )
    time.sleep( 3.0 )

    # Turn right
    bot.setMotorSpeeds( speed, -speed )
    time.sleep( 1.0 )
        
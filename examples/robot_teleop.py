#! /usr/bin/python

import pibot
import time

TURN_TIME = 0.2

bot = pibot.PiBot()

while True:
    
    # Read commands from the user
    command = raw_input( ": " )
    command = command.strip().lower()
    
    if len( command ) > 0:
        
        commandLetter = command[ 0 ]
        
        if commandLetter == "f":
            bot.setMotorSpeeds( 128, 128 )
            
        elif commandLetter == "b":
            bot.setMotorSpeeds( -128, -128 )
            
        elif commandLetter == "l":
            bot.setMotorSpeeds( -128, 128 )
            time.sleep( TURN_TIME )
            bot.setMotorSpeeds( 0, 0 )
            
        elif commandLetter == "r":
            bot.setMotorSpeeds( 128, -128 )
            time.sleep( TURN_TIME )
            bot.setMotorSpeeds( 0, 0 )
            
        elif commandLetter == "s":
            bot.setMotorSpeeds( 0, 0 )
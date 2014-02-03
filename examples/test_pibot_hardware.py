#! /usr/bin/env python

import time
import os.path
import sys

import pygame
import pygame.mixer

import pibot

MUSIC_VOLUME = 0.5
TEST_TIME = 10.0

scriptPath = os.path.dirname( __file__ )

# Load test result sounds
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load( scriptPath + "/../data/sounds/drum_roll.mp3" )
pygame.mixer.music.set_volume( MUSIC_VOLUME )
pygame.mixer.music.play()

# Connect to the PiBot
bot = pibot.PiBot()

testStartTime = time.time()

while time.time() - testStartTime < TEST_TIME:
    
    curTime = time.time() - testStartTime
    
    # Set motor speeds
    if int( curTime )%2 == 0:
        
        bot.setMotorSpeeds( 192, -192 )
        bot.setStepperSpeed( 255 )
        
        for pixelIdx in range( bot.NUM_NEO_PIXELS ):
            
            bot.setNeoPixelColour( pixelIdx, 128, 0, 0 )
        
    else:
        
        bot.setMotorSpeeds( -192, 192 )
        bot.setStepperSpeed( -255 )
        
        for pixelIdx in range( bot.NUM_NEO_PIXELS ):
            
            bot.setNeoPixelColour( pixelIdx, 0, 0, 128 )

    # Set servo angle
    bot.setServoAngle( (curTime / TEST_TIME) * 180.0 )
    
    print "Ultrasonic distance =", bot.getUltrasonicDistance()
    
    time.sleep( 0.05 )

for pixelIdx in range( bot.NUM_NEO_PIXELS ):
            
    bot.setNeoPixelColour( pixelIdx, 0, 128, 0 )
    
del bot
      
pygame.mixer.music.load( scriptPath + "/../data/sounds/success.mp3" )
pygame.mixer.music.set_volume( MUSIC_VOLUME )
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass
      

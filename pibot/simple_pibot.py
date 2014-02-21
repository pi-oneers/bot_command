
import copy
import time
import spidev

#---------------------------------------------------------------------------------------------------
class PiBot:
    """A class to communicate with and control the PiBot interface board"""
    
    MAX_ABS_MOTOR_SPEED = 255
    MAX_ABS_STEPPER_SPEED = 255
    MIN_SERVO_ANGLE = 0
    MAX_SERVO_ANGLE = 180
    NUM_NEO_PIXELS = 8
    
    #-----------------------------------------------------------------------------------------------
    def __init__( self ):

        self.spi = spidev.SpiDev()
        self.spi.open( 0, 0 )
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
        
        self.neoPixelData = [ ( 0, 0, 0 ) for i in range( self.NUM_NEO_PIXELS ) ]
        
    #-----------------------------------------------------------------------------------------------
    def __del__( self ):
    
        # Put the robot into a safe state ( motor speeds 0 )
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 3, 0 ] )
        self.spi.xfer( [ 4, 0 ] )
        self.spi.xfer( [ 6, 0 ] )
        
    #-----------------------------------------------------------------------------------------------
    def setMotorSpeeds( self, leftMotorSpeed, rightMotorSpeed ):
        
        # Constrain the motor speeds
        leftMotorSpeed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( leftMotorSpeed ), self.MAX_ABS_MOTOR_SPEED ) )
        rightMotorSpeed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( rightMotorSpeed ), self.MAX_ABS_MOTOR_SPEED ) )
        
        # Split up speed and direction
        leftMotorDirection = 0
        if leftMotorSpeed < 0:
            leftMotorDirection = 1
            leftMotorSpeed = -leftMotorSpeed
        
        rightMotorDirection = 0
        if rightMotorSpeed < 0:
            rightMotorDirection = 1
            rightMotorSpeed = -rightMotorSpeed
        
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 1, leftMotorDirection ] )
        self.spi.xfer( [ 2, rightMotorDirection ] )
        self.spi.xfer( [ 3, leftMotorSpeed ] )
        self.spi.xfer( [ 4, rightMotorSpeed ] )

    #-----------------------------------------------------------------------------------------------
    def setStepperSpeed( self, speed ):
        
        # Constrain the speed
        speed = max( -self.MAX_ABS_STEPPER_SPEED, min( int( speed ), self.MAX_ABS_STEPPER_SPEED ) )
        
        # Split up speed and direction
        stepperDirection = 0
        if speed < 0:
            stepperDirection = 1
            speed = -speed
        
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 5, stepperDirection ] )
        self.spi.xfer( [ 6, speed ] )
        
    #-----------------------------------------------------------------------------------------------
    def setServoAngle( self, angle ):
        
        # Constrain the angle
        angle = max( self.MIN_SERVO_ANGLE, min( int( angle ), self.MAX_SERVO_ANGLE ) )
        
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 7, angle ] )
    
    #-----------------------------------------------------------------------------------------------
    def getUltrasonicDistance( self ):
        
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 100 ] )    # Request ultrasonic read
        time.sleep( 0.001 )
        return self.spi.xfer( [ 0 ] )
        
    #-----------------------------------------------------------------------------------------------
    def setNeoPixelColour( self, pixelIdx, r, g, b ):
        
        if pixelIdx >= 0 and pixelIdx < len( self.neoPixelData ):
            
            r = max( 0, min( int( r ), 255 ) )
            g = max( 0, min( int( g ), 255 ) )
            b = max( 0, min( int( b ), 255 ) )
            
            self.neoPixelData[ pixelIdx ] = ( r, g, b )
            
            self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
            
            self.spi.xfer( [ 8 + 3*pixelIdx, r ] )
            self.spi.xfer( [ 8 + 3*pixelIdx + 1, g ] )
            self.spi.xfer( [ 8 + 3*pixelIdx + 2, b ] )
            
            #for pixelIdx, pixelData in enumerate( self.neoPixelData ):
            
                #self.spi.xfer( [ 8 + 3*pixelIdx, pixelData[ 0 ] ] )
                #self.spi.xfer( [ 8 + 3*pixelIdx + 1, pixelData[ 1 ] ] )
                #self.spi.xfer( [ 8 + 3*pixelIdx + 2, pixelData[ 2 ] ] )
      
    #-----------------------------------------------------------------------------------------------
    def colorWipe( self, color, wait ):
        
        # Fill the dots one after the other with a color
        for pixelIdx in range( self.NUM_NEO_PIXELS ):
            
            self.setNeoPixelColour( pixelIdx, color[ 0 ], color[ 1 ], color[ 2 ] )
            time.sleep( wait )
            
    #-----------------------------------------------------------------------------------------------
    def rainbow( self, wait ):
  
        for j in range( 256 ):
            
            for pixelIdx in range( self.NUM_NEO_PIXELS ):
                
                color = self.Wheel( (pixelIdx+j) % 256 )
                self.setNeoPixelColour( pixelIdx, color[ 0 ], color[ 1 ], color[ 2 ] )
                
            time.sleep( wait )

    #-----------------------------------------------------------------------------------------------
    # Slightly different, this makes the rainbow equally distributed throughout
    def rainbowCycle( self, wait ):
        
        for j in range( 256*5 ):    # 5 cycles of all colors on wheel

            for pixelIdx in range( self.NUM_NEO_PIXELS ):
                
                color = self.Wheel( ((pixelIdx * 256 /self.NUM_NEO_PIXELS) + j) % 256 )
                self.setNeoPixelColour( pixelIdx, color[ 0 ], color[ 1 ], color[ 2 ] )
                
            time.sleep( wait )

#//Theatre-style crawling lights.
#void theaterChase(uint32_t c, uint8_t wait) {
  #for (int j=0; j<10; j++) { //do 10 cycles of chasing
    #for (int q=0; q < 3; q++) {
      #for (int i=0; i < strip.numPixels(); i=i+3) {
        #strip.setPixelColor(i+q, c); //turn every third pixel on
      #}
      #strip.show();
     
      #delay(wait);
     
      #for (int i=0; i < strip.numPixels(); i=i+3) {
        #strip.setPixelColor(i+q, 0); //turn every third pixel off
      #}
    #}
  #}
#}

#//Theatre-style crawling lights with rainbow effect
#void theaterChaseRainbow(uint8_t wait) {
  #for (int j=0; j < 256; j++) { // cycle all 256 colors in the wheel
    #for (int q=0; q < 3; q++) {
        #for (int i=0; i < strip.numPixels(); i=i+3) {
          #strip.setPixelColor(i+q, Wheel( (i+j) % 255)); //turn every third pixel on
        #}
        #strip.show();
       
        #delay(wait);
       
        #for (int i=0; i < strip.numPixels(); i=i+3) {
          #strip.setPixelColor(i+q, 0); //turn every third pixel off
        #}
    #}
  #}
#}

    #-----------------------------------------------------------------------------------------------
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    def Wheel( self, wheelPos ):
    
        
    
        if wheelPos < 85:
            color = ( wheelPos*3, 255 - wheelPos*3, 0 )
        elif wheelPos < 170:
            wheelPos -= 85
            color = ( 255 - wheelPos*3, 0, wheelPos*3 )
        else:
            wheelPos -= 170
            color = ( 0, wheelPos*3, 255 - wheelPos*3 )
        
        return ( color[ 0 ] / 4, color[ 1 ] / 4, color[ 2 ] / 4 )
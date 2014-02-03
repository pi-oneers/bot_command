
import copy
import time
import spidev
import multiprocessing

#---------------------------------------------------------------------------------------------------
class ControlProcess( multiprocessing.Process ):
    
    #-----------------------------------------------------------------------------------------------
    def __init__( self, sharedDict, updateRateHz=50.0 ):
        
        multiprocessing.Process.__init__( self )
        
        self.spi = spidev.SpiDev()
        self.spi.open( 0, 0 )
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
        
        self.updateRateHz = updateRateHz
        if self.updateRateHz <= 0.0:
            self.updateRateHz = 1.0
        
        self.stopEvent = multiprocessing.Event()
        
        # Robot state variables
        self.sharedDict = sharedDict
        self.sharedDict[ "leftMotorDirection" ] = 0
        self.sharedDict[ "leftAbsMotorSpeed" ] = 0
        self.sharedDict[ "rightMotorDirection" ] = 0
        self.sharedDict[ "rightAbsMotorSpeed" ] = 0
        self.sharedDict[ "stepperDirection" ] = 0
        self.sharedDict[ "stepperAbsSpeed" ] = 0
        self.sharedDict[ "servoAngle" ] = 0
        self.sharedDict[ "lastUltrasonicDistance" ] = 0
        self.sharedDict[ "neoPixelData" ] = []

    #-----------------------------------------------------------------------------------------------
    def __del__( self ):
    
        # Put the robot into a safe state ( motor speeds 0 )
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 3, 0 ] )
        self.spi.xfer( [ 4, 0 ] )
        self.spi.xfer( [ 6, 0 ] )
      
    #-----------------------------------------------------------------------------------------------
    def stop( self ):
        self.stopEvent.set()

    #-----------------------------------------------------------------------------------------------
    def isStopped( self ):
        return self.stopEvent.is_set()
        
    #-----------------------------------------------------------------------------------------------
    def run( self ):
        
        while not self.isStopped():
            
            loopStartTime = time.time()
            
            self.transmitRobotState()
                
            maxLoopTime = 1.0/self.updateRateHz
            sleepTime = maxLoopTime - (time.time() - loopStartTime)
            if sleepTime > 0.0:
                time.sleep( sleepTime )

    #-----------------------------------------------------------------------------------------------
    def transmitRobotState( self ):
    
        self.spi.xfer( [ 0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer( [ 1, self.sharedDict[ "leftMotorDirection" ] ] )
        self.spi.xfer( [ 2, self.sharedDict[ "rightMotorDirection" ] ] )
        self.spi.xfer( [ 3, self.sharedDict[ "leftAbsMotorSpeed" ] ] )
        self.spi.xfer( [ 4, self.sharedDict[ "rightAbsMotorSpeed" ] ] )
        self.spi.xfer( [ 5, self.sharedDict[ "stepperDirection" ] ] )
        self.spi.xfer( [ 6, self.sharedDict[ "stepperAbsSpeed" ] ] )
        self.spi.xfer( [ 7, self.sharedDict[ "servoAngle" ] ] )
        
        neoPixelData = self.sharedDict[ "neoPixelData" ]
        for pixelIdx, pixelData in enumerate( neoPixelData ):
            
            self.spi.xfer( [ 8 + 3*pixelIdx, pixelData[ 0 ] ] )
            self.spi.xfer( [ 8 + 3*pixelIdx + 1, pixelData[ 1 ] ] )
            self.spi.xfer( [ 8 + 3*pixelIdx + 2, pixelData[ 2 ] ] )
        
        self.spi.xfer( [ 100 ] )    # Request ultrasonic read
        time.sleep( 0.001 )
        self.sharedDict[ "lastUltrasonicDistance" ] = self.spi.xfer( [ 0 ] )

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

        self.manager = multiprocessing.Manager()
        self.sharedDict = self.manager.dict()
    
        self.controlProcess = ControlProcess( self.sharedDict )
        self.controlProcess.start()
        
        self.neoPixelData = [ ( 0, 0, 0 ) for i in range( self.NUM_NEO_PIXELS ) ]
        self.sharedDict[ "neoPixelData" ] = copy.copy( self.neoPixelData )
        
    #-----------------------------------------------------------------------------------------------
    def __del__( self ):
        
        self.controlProcess.stop()
        self.controlProcess.join()
        
        del self.controlProcess
        
    #-----------------------------------------------------------------------------------------------
    def setMotorSpeeds( self, leftMotorSpeed, rightMotorSpeed ):
        
        # Constrain the motor speeds
        leftMotorSpeed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( leftMotorSpeed ), self.MAX_ABS_MOTOR_SPEED ) )
        rightMotorSpeed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( rightMotorSpeed ), self.MAX_ABS_MOTOR_SPEED ) )
        
        # Split up speed and direction
        if leftMotorSpeed >= 0:
            self.sharedDict[ "leftMotorDirection" ] = 0
        else:
            self.sharedDict[ "leftMotorDirection" ] = 1
            
        if rightMotorSpeed >= 0:
            self.sharedDict[ "rightMotorDirection" ] = 0
        else:
            self.sharedDict[ "rightMotorDirection" ] = 1
            
        self.sharedDict[ "leftAbsMotorSpeed" ] = abs( leftMotorSpeed )
        self.sharedDict[ "rightAbsMotorSpeed" ] = abs( rightMotorSpeed )

    #-----------------------------------------------------------------------------------------------
    def setStepperSpeed( self, speed ):
        
        # Constrain the speed
        speed = max( -self.MAX_ABS_STEPPER_SPEED, min( int( speed ), self.MAX_ABS_STEPPER_SPEED ) )
        
        # Split up speed and direction
        if speed >= 0:
            self.sharedDict[ "stepperDirection" ] = 0
        else:
            self.sharedDict[ "stepperDirection" ] = 1
        
        self.sharedDict[ "stepperAbsSpeed" ] = abs( speed )
        
    #-----------------------------------------------------------------------------------------------
    def setServoAngle( self, angle ):
        
        # Constrain the angle
        angle = max( self.MIN_SERVO_ANGLE, min( int( angle ), self.MAX_SERVO_ANGLE ) )
        self.sharedDict[ "servoAngle" ] = angle
    
    #-----------------------------------------------------------------------------------------------
    def getUltrasonicDistance( self ):
        
        return self.sharedDict[ "lastUltrasonicDistance" ]
        
    #-----------------------------------------------------------------------------------------------
    def setNeoPixelColour( self, pixelIdx, r, g, b ):
        
        if pixelIdx >= 0 and pixelIdx < len( self.neoPixelData ):
            
            r = max( 0, min( int( r ), 255 ) )
            g = max( 0, min( int( g ), 255 ) )
            b = max( 0, min( int( b ), 255 ) )
            
            self.neoPixelData[ pixelIdx ] = ( r, g, b )
            self.sharedDict[ "neoPixelData" ] = copy.copy( self.neoPixelData )
        
        
        
        
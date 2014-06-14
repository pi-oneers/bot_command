import spidev
import time

class PiBot:
    """A class to communicate with and control the PiBot interface board"""

    CMD_LEFT_MOTOR_DIR    = 1
    CMD_RIGHT_MOTOR_DIR   = 2
    CMD_LEFT_MOTOR_SPEED  = 3
    CMD_RIGHT_MOTOR_SPEED = 4
    
    MAX_ABS_MOTOR_SPEED   = 255
    MAX_ABS_STEPPER_SPEED = 255
    MIN_SERVO_ANGLE       = 0
    MAX_SERVO_ANGLE       = 180
    NUM_NEO_PIXELS        = 8

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open( 0, 0 )
        self.spi.max_speed_hz = 500000
        self.spi.mode = 0
        
        self.neoPixelData = [ ( 0, 0, 0 ) for i in range( self.NUM_NEO_PIXELS ) ]

    def __del__(self):
    
        # Put the robot into a safe state ( motor speeds 0 )
        self.spi.xfer([0x55, 0x55, 0x55 ] )    # Sync
        self.spi.xfer([self.CMD_LEFT_MOTOR_SPEED,  0])
        self.spi.xfer([self.CMD_RIGHT_MOTOR_SPEED, 0])

    def goForward(self, duration=1.0, speed=127):
        '''
        Move forwards. Defaults to driving forwards for one second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
        self.go(duration, speed, speed)
    
    def goBackward(self, duration=1.0, speed=127):
        '''
        Move backwards. Defaults to driving backwards for one second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''

        self.go(duration, -speed, -speed)
    
    def goLeft(self, duration=0.5, speed=127):
        '''
        Rotate left. Defaults to rotating anti-clockwise for half a second at a speed 
        of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
        self.go(duration, 0, speed)

    def goRight(self, duration=0.5, speed=127):
        '''
        Rotate right. Defaults to rotating clockwise for half a second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
        self.go(duration, speed, 0)

    def go(self, duration, left_speed, right_speed):
        ''' 
        Run motors separately with custom speed values for a set duration. 
        
        :param int left_speed: Left motor speed value: -127 to 127 (negative is backwards)
        :param int right_speed: Right motor speed value: -127 to 127 (negative is backwards)
        :param float duration: Duration in seconds.
        '''

        # Constrain the motor speeds
        left_speed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( left_speed ), self.MAX_ABS_MOTOR_SPEED ) )
        right_speed = max( -self.MAX_ABS_MOTOR_SPEED, min( int( right_speed ), self.MAX_ABS_MOTOR_SPEED ) )
        
        # Split up speed and direction
        left_direction = 0
        if left_speed < 0:
            left_direction = 1
            left_speed = -left_speed
        
        right_direction = 0
        if right_speed < 0:
            right_direction = 1
            right_speed = -right_speed
        
        self.spi.xfer([0x55, 0x55, 0x55 ]) # Sync
        self.spi.xfer([self.CMD_LEFT_MOTOR_DIR, left_direction])
        self.spi.xfer([self.CMD_RIGHT_MOTOR_DIR, right_direction])
        self.spi.xfer([self.CMD_LEFT_MOTOR_SPEED, left_speed])
        self.spi.xfer([self.CMD_RIGHT_MOTOR_SPEED, right_speed])

        time.sleep(duration)

        #reset to 0
        self.spi.xfer([0x55, 0x55, 0x55 ]) # Sync
        self.spi.xfer([self.CMD_LEFT_MOTOR_SPEED, 0])
        self.spi.xfer([self.CMD_RIGHT_MOTOR_SPEED, 0])
    
    def viewLeft(self, duration=0.5, speed=127):
        '''
        Pan camera left. Defaults to panning anti-clockwise for half a second at a speed 
        of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    def viewRight(self, duration=0.5, speed=127):
        '''
        Pan camera right. Defaults to panning clockwise for half a second at a speed 
        of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    def tiltView(self, angle):
        '''
        Tilt the camera to a specified angle. 
    
        :param int angle: Angle in degrees: 0 to 360 
        '''
    
    def getDistance(self):
        '''
        Read the distance of an object in front of the robot.
    
        :return: Distance in mm
        :rtype: int
        '''
    
    def setLedColour(self, number, colour):
        '''
        Set the colour of a particular LED.
    
        :param int number: LED number: 0 - 8
        :param string colour: RGB colour string e.g. "#FF0000" is red 
        '''
    def doLedColourWipe(self, colour, speed=127):
        '''
        Do a wiper effect of one colour.
    
        :param string colour: RGB colour string e.g. "#FF0000" is red 
        :param int speed: Relative speed: 0 to 127, defaults to 127
        '''
    def doLedRainbow(self, speed=127):
        '''
        Do a rainbow effect.
    
        :param int speed: Relative speed: 0 to 127, defaults to 127
        '''
    def doLedTheaterChase( self, colour, speed=127):
        '''
        Do theatre-style crawling lights of a particular colour.
    
        :param string colour: RGB colour string e.g. "#FF0000" is red 
        :param int speed: Relative speed: 0 to 127, defaults to 127
        '''
    
    def say(self, text):
        '''
        Say the specified text using text-to-speech.
    
        :param string text: Phrase or word to say.
        '''
    

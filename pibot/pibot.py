class PiBot:
    def goForward(self, duration=1.0, speed=127):
        '''
        Move forwards. Defaults to driving forwards for one second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    
    def goBackward(self, duration=1.0, speed=127):
        '''
        Move backwards. Defaults to driving backwards for one second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    
    def goLeft(self, duration=0.5, speed=127):
        '''
        Rotate left. Defaults to rotating anti-clockwise for half a second at a speed 
        of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    
    def goRight(self, duration=0.5, speed=127):
        '''
        Rotate right. Defaults to rotating clockwise for half a second at a speed of 127.
    
        :param float duration: Duration in seconds.
        :param int speed: Relative speed: 0 to 127 
        '''
    def go(self, left, right, duration):
        ''' 
        Run motors separately with custom speed values for a set duration. 
        
        :param int left: Left motor speed value: -127 to 127 (negative is backwards)
        :param int right: Right motor speed value: -127 to 127 (negative is backwards)
        :param float duration: Duration in seconds.
        '''
    
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
    

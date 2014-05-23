class Movement:
    def setSpeed(self, speed):
        '''
        Sets a relative motor speed for all movement. Does not turn on the motors. 
        Before this function is called for the first time the speed is 127.

        :param int speed: 0 to 127
        '''
    def goForward(self, duration=1.0):
        '''
        Move forward for a set duration that defaults to 1 second.

        :param float duration: Duration in seconds.
        '''

    def goBackward(self, duration=1.0):
        '''
        Move backwards for a set duration that defaults to 1 second.

        :param float duration: Duration in seconds.
        '''

    def turnLeft(self, duration=0.5):
        '''
        Rotate left for the specified duration that defaults to half a second.

        :param float duration: Duration in seconds.
        '''

    def turnRight(self, duration=0.5):
        '''
        Rotate right for the specified duration that defaults to half a second.


        :param float duration: Duration in seconds.
        '''
    def runMotors(self, left, right, duration):
        ''' 
        Run motors with custom speed values for a set duration. This ignores the speed 
        value set by setSpeed.
        
        :param int left: Left motor speed value: -127 to 127 (negative is backwards)
        :param int right: Right motor speed value: -127 to 127 (negative is backwards)
        :param float duration: Duration in seconds.
        '''

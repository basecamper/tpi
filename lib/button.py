from enum import Enum
import RPi.GPIO as GPIO

from lib.log import Log

class Button(Enum):
   NONE = 0
   UP = 1
   DOWN = 2
   LEFT = 3
   RIGHT = 4
   PRESS = 5
   KEY1 = 6
   KEY2 = 7
   KEY3 = 8

ButtonMap = { # PINS
   Button.UP:     6,
   Button.DOWN:   19,
   Button.LEFT:   5,
   Button.RIGHT:  26,
   Button.PRESS:  13,
   Button.KEY1:   21,
   Button.KEY2:   20,
   Button.KEY3:   16
}

class ButtonHandler( Log ):
   def __init__( self, callback ):
      Log.__init__( self, "ButtonHandler" )
      GPIO.setmode(GPIO.BCM)
      self.parentCallback = callback
      for v in ButtonMap.values():
         GPIO.setup(v,GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up !
         GPIO.add_event_detect(v, GPIO.RISING, callback=self.buttonDown, bouncetime=200)
   
   def __del__(self):
      self.logStart( "__del__" )
      self.log( "GPIO cleanup" )
      GPIO.cleanup()
      self.logEnd()
   
   def _getButtonFromChannel( self, channel ):
      self.logStart( "_getButtonFromChannel","channel: {c}".format( c=channel ) )
      for k, v in ButtonMap.items():
         if v == channel:
            self.logEnd( "returning button {b}".format( b=k ) )
            return k
      self.logEnd( printMessage=False )
   
   def buttonDown( self, channel ):
      self.logStart( "buttonDown channel: {c}".format( c=channel ) )
      self.parentCallback( self._getButtonFromChannel( channel ) )
      self.logEnd()
      
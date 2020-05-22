from enum import Enum
import RPi.GPIO as GPIO
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

class ButtonHandler():
   def __init__( self, callback ):
      GPIO.setmode(GPIO.BCM)
      self.parentCallback = callback
      for v in ButtonMap.values():
         GPIO.setup(v,GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up !
         GPIO.add_event_detect(v, GPIO.RISING, callback=self.buttonDown, bouncetime=200)
   
   def __del__(self):
      GPIO.cleanup()
   
   def _getButtonFromChannel( self, channel ):
      for k, v in ButtonMap.items():
         if v == channel:
            return k
   
   def buttonDown( self, channel ):
      self.parentCallback( self._getButtonFromChannel( channel ) )
      
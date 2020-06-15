from lib.screen import ScreenElement
from lib.screen.screenColor import Color
from time import localtime, strftime

class CurrentTimeElement(ScreenElement):
   def __init__( self, dateFormatString ):
      ScreenElement.__init__( self )
      self.text = "time"
      self.color = Color.BLACKWHITE 
      self.dateFormatString = dateFormatString
   
   def run(self):
      self.text = strftime( self.dateFormatString, localtime() )
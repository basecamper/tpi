from time import localtime, strftime

from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement

class CurrentTimeElement(ScreenElement):
   def __init__( self, dateFormatString ):
      ScreenElement.__init__( self )
      self.text = "time"
      self.color = Color.BLACKWHITE 
      self.dateFormatString = dateFormatString
   
   def run(self):
      self.text = strftime( self.dateFormatString, localtime() )
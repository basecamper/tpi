from typing import Callable
from datetime import datetime
from lib.procHandler import ProcHandler
from lib.screen import ScreenElement
from lib.log import Log


class PollingElement( ScreenElement ):
   def __init__( self, osCommand = None, interval : int = 5, timeout : int = 3 ):
      super().__init__()
      self.dataChildElement = ScreenElement()
      self.addChild( self.dataChildElement )
      self.osCommand = osCommand
      self.dataProcHandler = ProcHandler( self.osCommand.getCommand(),
                                          self._procResult,
                                          interval,
                                          timeout )
   def run( self ):
      super().run()
      self.dataProcHandler.run()
   
   def _procResult( self, stdout, stderr ):
      #try:
         self.dataChildElement.text, self.dataChildElement.color = self.osCommand.parseFunction( stdout, stderr )
      #   Log.debug("PollingElement._procResult() new text '{text}'".format( text=self.dataChildElement.text ))
      #except Exception as e:
      #   Log.debug("ERROR parsing")
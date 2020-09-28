from typing import Callable
from datetime import datetime

from lib.log import Log
from lib.procHandler import ProcHandler
from lib.screen.element import ScreenElement


class PollingElement( ScreenElement, Log ):
   
   def __init__( self, osCommand = None, cooldown : int = 5, timeout : int = 3 ):
      ScreenElement.__init__( self )
      Log.__init__( self, className="PollingElement" )
      self.dataChildElement = ScreenElement()
      self.addChild( self.dataChildElement )
      self.osCommand = osCommand
      self.dataProcHandler = ProcHandler( command=self.osCommand.getCommand(),
                                          callback=self._procResult,
                                          cooldown=cooldown,
                                          timeout=timeout )
   
   def run( self ):
      self.dataProcHandler.run()
      super().run()
   
   def _procResult( self, stdout, stderr ):
      self.dataChildElement.text, self.dataChildElement.color = self.osCommand.parseFunction( stdout, stderr )
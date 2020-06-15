from typing import Callable
from datetime import datetime
from lib.procHandler import ProcHandler
from lib.screen import ScreenElement
from lib.log import Log


class PollingElement( ScreenElement, Log ):
   def __init__( self, osCommand = None, interval : int = 5, timeout : int = 3 ):
      ScreenElement.__init__( self )
      Log.__init__( self, className="PollingElement" )
      self.dataChildElement = ScreenElement()
      self.addChild( self.dataChildElement )
      self.osCommand = osCommand
      self.dataProcHandler = ProcHandler( command=self.osCommand.getCommand(),
                                          callback=self._procResult,
                                          interval=interval,
                                          timeout=timeout )
   def run( self ):
      self.dataProcHandler.run()
      super().run()
   
   def _procResult( self, stdout, stderr ):
      #try:
         self.dataChildElement.text, self.dataChildElement.color = self.osCommand.parseFunction( stdout, stderr )
      #   Log.debug("PollingElement._procResult() new text '{text}'".format( text=self.dataChildElement.text ))
      #except Exception as e:
      #   Log.debug("ERROR parsing")
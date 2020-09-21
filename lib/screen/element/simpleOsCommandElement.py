from lib.procHandler import ProcHandler
from lib.log import Log
from lib.screen.element import ScreenElement

from lib.screen.textConst import TEXT, COLOR

class SimpleOsCommandElement( ScreenElement, Log ):
   
   def __init__( self,
                 text : str,
                 button : object,
                 command : list,
                 cooldown : int = 0,
                 timeout : int = 3,
                 callback : object = None ):
      
      ScreenElement.__init__( self )
      Log.__init__( self, "SimpleOsCommandElement" )
      
      self._commandText = text
      self._button = button
      self._command = command
      self._parentCallback = callback
      self._procHandler = ProcHandler( command=command,
                                       onSuccess=self._onSuccess,
                                       onError=self._onError,
                                       cooldown=cooldown,
                                       timeout=timeout )
      self._finishedProcess = None
      self._dataElement = ScreenElement()
      self.addChild( self._dataElement )
      self._resetText()
   
   def _resetText( self ):
      self._dataElement.text, self._dataElement.color = self._commandText, COLOR.DEFAULT
   
   def onButtonDown( self, button ):
      if button == self._button:
         if not self._procHandler.isProcessing():
            self._procHandler.run()
   
   def _onSuccess( self ):
      self._dataElement.color = COLOR.OK
   
   def _onError( self ):
      self._dataElement.color = COLOR.ERROR

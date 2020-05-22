from lib.screen import ScreenElement
from lib.screen.pollingElement import PollingElement
from lib.procHandler import ProcHandler
from lib.screen.screenColor import Color

class ExecuteCommandElement( ScreenElement ):
   def __init__( self,
                 text : str,
                 startButton : object,
                 osCommand : object,
                 stopButton : object = None,
                 interval=10,
                 timeout=3 ):
      super().__init__()
      self.startButton = startButton
      self.stopButton = stopButton
      self.osCommand = osCommand
      
      self.dataChild = ScreenElement( text=text, color=Color.DEFAULT )
      self.addChild( self.dataChild )
      
      self.started = None # keep track of the pushed buttons to be able to switch in case no 
      
      self.startProcHandler = ProcHandler( self.osCommand.getStartCommand(), self._procStart, 1, 3 )
      self.stopProcHandler = (    ProcHandler( self.osCommand.getStopCommand(), self._procStop, 1, 3 )
                               if self.osCommand.getStopCommand() else None )
      self.statusProcHandler = (    ProcHandler( self.osCommand.getStatusCommand(), self._procStatus, 1, 3 )
                                 if self.osCommand.getStatusCommand() else None )
   
   def start( self ):
      if self.startProcHandler:
         self.startProcHandler.run()
      self.started = True
   
   def stop( self ):
      if self.stopProcHandler:
         self.stopProcHandler.run()
      self.started = False
      
   
   def onButtonDown( self, button ):
      if button == self.startButton:
         if not self.stopButton:
            if not self.started:
               self.start()
            else:
               self.stop()
         else:
            self.start()
      
      if button == self.stopButton:
         self.stop()
      super().onButtonDown( button )
   
   def _procStart( self, stdout, stderr ):
      text, color = self.osCommand.parseStart( stdout, stderr )
      if color:
         self.dataChild.color = color
   def _procStop( self, stdout, stderr ):
      pass
   def _procStatus( self, stdout, stderr ):
      try:
         self.dataChild.text, self.dataChild.color = self.pollStatusCommand.parseFunction( stdout, stderr )
         Log.debug("PollingElement._procResult() new text '{text}'".format( text=self.dataChildElement.text ))
      except Exception as e:
         Log.debug("ERROR parsing")
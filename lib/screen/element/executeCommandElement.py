from lib.procHandler import ProcHandler
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.pollingElement import PollingElement

class ExecuteCommandElement( ScreenElement ): # depreciated
   
   def __init__( self,
                 text : str,
                 startButton : object,
                 osCommand : object,
                 stopButton : object = None,
                 cooldown=10,
                 timeout=3 ):
      
      ScreenElement.__init__( self )
      self.startButton = startButton
      self.stopButton = stopButton
      self.osCommand = osCommand
      
      self.dataChild = ScreenElement( text=text, color=Color.DEFAULT )
      self.addChild( self.dataChild )
      
      self.started = None # keep track of the pushed buttons to be able to switch in case no 
      
      self.startProcHandler = ProcHandler( command=self.osCommand.getStartCommand(),
                                           callback=self._procStart,
                                           cooldown=1,
                                           timeout=3 )
      self.stopProcHandler = (    ProcHandler( command=self.osCommand.getStopCommand(),
                                               callback=self._procStop,
                                               cooldown=1,
                                               timeout=3 )
                               if self.osCommand.getStopCommand() else None )
      self.statusProcHandler = (    ProcHandler( command=self.osCommand.getStatusCommand(),
                                                 callback=self._procStatus,
                                                 interval=1,
                                                 timeout=3 )
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
from lib import osCommand
from lib import osPollCommand
from lib.glob import GlobalRuntime
from lib.log import Log
from lib.button import Button
from lib.procHandler import ProcHandler
from lib.screen import ScreenElement
from lib.screen.currentTimeElement import CurrentTimeElement
from lib.screen.pollingElement import PollingElement
from lib.screen.executeCommandElement import ExecuteCommandElement
from lib.screen.mainMenu import MainMenu
from lib.screen.screenColor import Color
from enum import Enum


   

class Overview( ScreenElement, Log ):

   def __init__( self ):
      ScreenElement.__init__( self,
                              children=[ ScreenElement( children=[ CurrentTimeElement( "%d.%m  %H:%M:%S" ) ],
                                                        isEndingLine=True ),
                                         ScreenElement( children=[ ScreenElement( text="GPU ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=osPollCommand.GetGPUTempCommand, interval=10, timeout=3 ),
                                                                   ScreenElement( text=" ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=osPollCommand.GetGPUMemUsageCommand, interval=10, timeout=3 )
                                                                 ],
                                                        isEndingLine=True ),
                                         ScreenElement( children=[ ScreenElement( text="CPU ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=osPollCommand.GetCPUTempCommand, interval=10, timeout=3 ) ],
                                                        isEndingLine=True ) ],
                              buttonProcMap={ Button.PRESS : self.okProc } )
      Log.__init__( self, "Overview" )
      self.menu = MainMenu()
      self.statusLine = ScreenElement( isEndingLine=True )
      
      self.addChild( self.menu )
      self.addChild( self.statusLine )
      
      self.splashProcHandler = ProcHandler( command=osCommand.DisplaySplashImageCommand.getStartCommand() )
      
      self.splashDisplayed = False
      self.enableSplash()
   
   def run( self ):
      self.logStart("run")
      if not self.splashDisplayed:
         super().run()
      
      status, color = Log.popStatus()
      
      if status:
         self.statusLine.text = status
         self.statusLine.color = color
      self.logEnd()
   
   def okProc( self, button ):
      self.logStart("okProc")
      self.toggleSplash()
      self.logEnd()
   
   def toggleSplash( self ):
      self.logStart("toggleSplash")
      if self.splashDisplayed:
         self.disableSplash()
      else:
         self.enableSplash()
      self.logEnd()
   
   def enableSplash( self ):
      self.logStart("enableSplash")
      GlobalRuntime.refreshScreen = False
      self.setEnablePropagation( False )
      self.splashDisplayed = True
      self.splashProcHandler.run()
      self.logEnd()
   
   def disableSplash( self ):
      self.logStart("disableSplash")
      GlobalRuntime.refreshScreen = True
      self.setEnablePropagation( True )
      self.splashDisplayed = False
      self.logEnd()
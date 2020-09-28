from enum import Enum

from lib.osPollCommand import GetGPUTempCommand, GetGPUMemUsageCommand, GetCPUTempCommand
from lib.glob import GlobalRuntime, Global
from lib.log import Log
from lib.button import Button
from lib.procHandler import ProcHandler
from lib.screen.mainMenu import MainMenu
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.currentTimeElement import CurrentTimeElement
from lib.screen.element.pollingElement import PollingElement

CMD_DISPLAY_SPLASH = ['dd','if=/opt/splash.bmp','of=/dev/fb1','bs=655555','count=1','status=none']

class Overview( ScreenElement, Log ):

   def __init__( self ):
      ScreenElement.__init__( self,
                              children=[ ScreenElement( children=[ CurrentTimeElement( "%d.%m  %H:%M:%S" ) ],
                                                        isEndingLine=True ),
                                         ScreenElement( children=[ ScreenElement( text="GPU ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=GetGPUTempCommand,
                                                                                   cooldown=10,
                                                                                   timeout=3 ),
                                                                   ScreenElement( text=" ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=GetGPUMemUsageCommand,
                                                                                   cooldown=10,
                                                                                   timeout=3 )
                                                                 ],
                                                        isEndingLine=True ),
                                         ScreenElement( children=[ ScreenElement( text="CPU ", color=Color.DEFAULT ),
                                                                   PollingElement( osCommand=GetCPUTempCommand,
                                                                                   cooldown=10,
                                                                                   timeout=3 ) ],
                                                        isEndingLine=True ) ],
                              buttonDownMap={ Button.PRESS : self.toggleSplash } )
      Log.__init__( self, "Overview" )
      self.menu = MainMenu()
      self.statusLine = ScreenElement( isEndingLine=True )
      
      self.addChild( self.menu )
      self.addChild( self.statusLine )
      
      self.splashProcHandler = ProcHandler( command=CMD_DISPLAY_SPLASH )
      
      self.splashDisplayed = False
      if Global.DISPLAY_SPLASH:
         self.enableSplash()
   
   def run( self ):
      self.logStart()
      if not self.splashDisplayed:
         super().run()
      
      status, color = Log.popStatus()
      
      if status:
         self.statusLine.text = status
         self.statusLine.color = color
      self.logEnd()
   
   def toggleSplash( self, button ):
      self.logStart()
      if self.splashDisplayed:
         self.disableSplash()
      else:
         self.enableSplash()
      self.logEnd()
   
   def enableSplash( self ):
      self.logStart()
      GlobalRuntime.refreshScreen = False
      self.setExclusivePropagation( True )
      self.setEnablePropagation( False )
      self.splashDisplayed = True
      self.splashProcHandler.run()
      self.logEnd()
   
   def disableSplash( self ):
      self.logStart()
      GlobalRuntime.refreshScreen = True
      self.setExclusivePropagation( False )
      self.setEnablePropagation( True )
      self.splashDisplayed = False
      self.logEnd()

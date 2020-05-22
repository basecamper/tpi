from lib import osCommand
from lib import osPollCommand
from lib.glob import GlobalRuntime
from lib.log import Log
from lib.button import Button
from lib.screen import ScreenElement, ScreenReturn
from lib.screen.currentTimeElement import CurrentTimeElement
from lib.screen.pollingElement import PollingElement
from lib.screen.executeCommandElement import ExecuteCommandElement
from lib.screen.menu import Menu
from lib.screen.screenColor import Color
from enum import Enum

def getMainElements():
   return [ ScreenElement( children=[ CurrentTimeElement( "%d.%m  %H:%M:%S" ) ],
                           isEndingLine=True ),
            ScreenElement( children=[ ScreenElement( text="GPU ", color=Color.DEFAULT ),
                                      PollingElement( osCommand=osPollCommand.GetGPUTempCommand, interval=10, timeout=3 ),
                                      ScreenElement( text=" ", color=Color.DEFAULT ),
                                      PollingElement( osCommand=osPollCommand.GetGPUMemUsageCommand, interval=10, timeout=3 )
                                    ],
                           isEndingLine=True ),
            ScreenElement( children=[ ScreenElement( text="CPU ", color=Color.DEFAULT ),
                                      PollingElement( osCommand=osPollCommand.GetCPUTempCommand, interval=10, timeout=3 ) ],
                           isEndingLine=True )
          ]

class Overview(ScreenElement):
   def __init__( self ):
      Log.debug( "Overview init" )
      super().__init__( children=getMainElements() )
      self.splashImageMenuItem = ExecuteCommandElement( text="splash",
                                                        osCommand=osCommand.DisplaySplashImageCommand,
                                                        startButton=Button.PRESS )
      self.menu = Menu( menuItems=[ self.splashImageMenuItem,
                                    ExecuteCommandElement( text="wpa_supplicant",
                                                           osCommand=osCommand.WpaSupplicantCommand,
                                                           startButton=Button.PRESS ),
                                    ExecuteCommandElement( text="wlan0 interface",
                                                           osCommand=osCommand.EnableWlanInterfaceCommand,
                                                           startButton=Button.PRESS ),
                                    ExecuteCommandElement( text="wlan0 wifi",
                                                           osCommand=osCommand.EnableWlanWifiCommand,
                                                           startButton=Button.PRESS ),
                                    ExecuteCommandElement( text="poweroff",
                                                           osCommand=osCommand.PoweroffCommand,
                                                           startButton=Button.PRESS )
                                  ],
                        prevButton=Button.UP,
                        nextButton=Button.DOWN )
      self.addChild( self.menu )
      self.onButtonDown( Button.PRESS )
   
   def run( self ):
      if not self.splashImageMenuItem.started:
         super().run()
   
   def onButtonDown( self, button ):
      Log.debug( "Overview onButtonDown button: {button}".format( button=button ) )
      if self.splashImageMenuItem.started:
         self.splashImageMenuItem.onButtonDown( button )
      else:
         super().onButtonDown( button )
      
      GlobalRuntime.lockScreen = bool( self.splashImageMenuItem.started )
         
      return ScreenReturn.OK
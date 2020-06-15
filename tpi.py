import time
import sys

from lib.button import ButtonHandler
from lib.screenManager import ScreenManager
from lib.glob import Global, GlobalRuntime

class Control:
   
   screenManager = None
   buttonHandler = None
   
   def __init__( self ):
      if Control.screenManager or Control.buttonHandler: # "enforce singleton..."
         raise Exception( "initialize Control once!")
      Control.screenManager = ScreenManager()
      Control.buttonHandler = ButtonHandler( self.screenManager.onButtonDown )
      GlobalRuntime.setAsyncScreenRefreshCallback( Control.procAsyncRefresh )
   
   def __del__( self ):
      del( Control.screenManager )
      del( Control.buttonHandler )
      Control.screenManager = None
      Control.buttonHandler = None
   
   def run( self ):
      while 1:
         Control.screenManager.run()
         time.sleep( Global.MAIN_RUN_SECONDS )
   
   @staticmethod
   def procAsyncRefresh():
      Control.screenManager.run()

if __name__ == "__main__":
   artc = len(sys.argv)
   if "debug" in sys.argv:
      Global.DEBUG_PRINT = True
      Global.MAIN_RUN_SECONDS = 180
   
   try:
      c = Control()
      c.run()
   
   except KeyboardInterrupt as e:
      del(c)
      sys.stderr.write("KeyboardInterrupt\n")
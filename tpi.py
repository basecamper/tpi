import time
from lib.button import ButtonHandler
from lib.screenManager import ScreenManager
from lib.glob import Global


class Control:
   def __init__(self):
      self.screenManager = ScreenManager()
      self.buttonHandler = ButtonHandler( self.screenManager.onButtonDown )
   
   def run(self):
      while 1:
         self.screenManager.run()
         time.sleep( Global.MAIN_RUN_SECONDS )

if __name__ == "__main__":
   try:
      c = Control()
      c.run()
   except KeyboardInterrupt as e:
      print("quit")
      del(c)
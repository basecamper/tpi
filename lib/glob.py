from enum import Enum

SYSTEM_OK = 0

class Global:
   DEBUG = False # disable curses screen / show Log.debug messages
   DEBUG_PRINT = False # keep printing debug messages to stderr
   MAIN_RUN_SECONDS = 0.2 # run() interval
   CONFIG_FILE = "./config.json"

class GlobalRuntime:
   # perform run() / refresh curses screen each interval
   # e.g. set to false to not print anything while the splash image is displayed
   refreshScreen = True
   
   # registered in screenHandler to trigger a run()
   _asyncScreenRefreshCallback = None
   
   @staticmethod
   def setAsyncScreenRefreshCallback( func : object ):
      GlobalRuntime._asyncScreenRefreshCallback = func
   
   # called by any module to cause an async screen refresh
   @staticmethod
   def run():
      if GlobalRuntime._asyncScreenRefreshCallback:
         GlobalRuntime._asyncScreenRefreshCallback()
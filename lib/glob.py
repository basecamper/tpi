from enum import Enum

SYSTEM_OK = 0

class Global:
   DEBUG = False # disable curses screen / show Log.debug messages
   DEBUG_PRINT = False # keep printing debug messages to stderr
   DISPLAY_SPLASH = False # auto-show splash image after startup
   MAIN_RUN_SECONDS = 0.2 # run() interval
   CONFIG_FILE = "./config.json"
   LOG_REDUCE_INDENT = 0

class RUNTIME_CONFIG_KEY:
   keymap = "keymap"
   keyTimeout = "keyTimeout"

class GlobalRuntime:
   
   # gets set from SetRuntimeConfigElement
   _configDict = {}
   
   # perform run() / refresh curses screen each interval
   # e.g. set to false to not print anything while the splash image is displayed
   refreshScreen = True
   
   # registered in screenHandler to trigger a run()
   _asyncScreenRefreshCallback = None
   
   @staticmethod
   def setRuntimeConfig( key : str, value : str ):
      if len( key ) > 0:
         GlobalRuntime._configDict[ key ] = value
   
   @staticmethod
   def hasRuntimeConfig( key : str ):
      return bool( key in GlobalRuntime._configDict )
   
   @staticmethod
   def getRuntimeConfig( key : str ):
      if GlobalRuntime.hasRuntimeConfig( key ):
         return GlobalRuntime._configDict[ key ]
      else:
         return None
   
   @staticmethod
   def setAsyncScreenRefreshCallback( func : object ):
      GlobalRuntime._asyncScreenRefreshCallback = func
   
   # called by any module to cause an async screen refresh
   @staticmethod
   def run():
      if GlobalRuntime._asyncScreenRefreshCallback:
         GlobalRuntime._asyncScreenRefreshCallback()

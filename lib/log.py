from lib.glob import Global

class Log:
   @staticmethod
   def debug( msg ):
      if Global.DEBUG:
         print( msg )
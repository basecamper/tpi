from lib.log import Log

class KeyStroker( Log ):
   def __init__( self ):
      Log.__init__( self, "KeyStroker" )
   def sendCharacters( self, text : str ):
      pass
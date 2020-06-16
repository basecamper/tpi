from lib.log import Log
from lib.tools import BitState

class HasState( Log ):
   
   def __init__( self ):
      Log.__init__( self, "HasState" )
      self.clearStates()
   
   def clearStates( self ):
      self.logStart( "clearStates" )
      self.logEnd( printMessage=False )
      self._bitState = 0
   
   def hasState( self, state ):
      self.logStart( "hasState","{s} ( {b} )".format( s=bin( self._bitState ), b=bin( state ) ) )
      self.logEnd( message="returning {r}".format(  r=BitState.hasBit( self._bitState, state ) ))
      return BitState.hasBit( self._bitState, state )
   
   def setState( self, state ):
      self.logStart( "setState","{s} + {b}".format( s=bin( self._bitState ), b=bin( state ) ) )
      self._bitState = BitState.setBit( self._bitState, state )
      self.logEnd( "{s}".format( s=bin( self._bitState ) ) )
   
   def delState( self, state ):
      self.logStart( "delState","{s} - {b}".format( s=bin( self._bitState ), b=bin( state ) ) )
      self._bitState = BitState.delBit( self._bitState, state )
      self.logEnd( "{s}".format( s=bin( self._bitState ) ) )
   
   def toggleState( self, state ):
      if self.hasState( state ):
         self._bitState = BitState.delBit( self._bitState, state )
      else:
         self._bitState = BitState.setBit( self._bitState, state )

import time

EMPTY_STRING = ""

def getMsTimestamp():
   return int(round(time.time() * 1000))

class BitState():
   
   @staticmethod
   def hasBit( binValue, binCompare ):
      return binValue & binCompare != 0
   
   @staticmethod
   def setBit( binValue, binCompare ):
      if BitState.hasBitSet( binValue, binCompare ):
         return binValue
      return binValue | binCompare
   
   @staticmethod
   def delBit( binValue, binCompare ):
      if not BitState.hasBitSet( binValue, binCompare ):
         return binValue
      return binValue ^ binCompare

class HasStep( object ):
   
   def __init__( self, startStep : int = 0 ):
      object.__init__( self )
      self._startStep = startStep
      self._currentStep = self._startStep
   
   def hasStep( self, step : int ):
      return self._currentStep == step
   
   def getStep( self ):
      return self._currentStep
   
   def setStep( self, step : int ):
      self._currentStep = step
   
   def startStep( self ):
      self._currentStep = self._startStep


class HasState( object ):
   
   def __init__( self ):
      object.__init__( self )
      self._bitState = 0
   
   def hasState( self, state ):
      return BitState.hasBit( self._bitState, state )
   
   def setState( self, state ):
      self._bitState = BitState.setBit( self._bitState, state )
   
   def delState( self, state ):
      self._bitState = BitState.delBit( self._bitState, state )
   
   def toggleState( self, state ):
      if self.hasState( state ):
         self._bitState = BitState.delBit( self._bitState, state )
      else:
         self._bitState = BitState.setBit( self._bitState, state )
      
   
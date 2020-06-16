from lib.log import Log
from lib.tools import BitState

class HasStep( Log ):
   
   def __init__( self, startStep : int = -1 ):
      Log.__init__( self, "HasStep" )
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

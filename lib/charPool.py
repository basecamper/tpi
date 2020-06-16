from lib.hasState import HasState
from lib.hasStep import HasStep
from lib.log import Log

class CharPool( Log ):
   
   def __init__( self, poolString ):
      Log.__init__( self, "CharPool" )
      self._poolString = poolString
      self._poolStringIndex = 0
      self._poolStringLength = len( self._poolString )
   
   def getIndex( self ):
      return self._poolStringIndex
   
   def getCharCount( self ):
      return self._poolStringLength
   
   def evalSetIndex( self, index : int = None, delta : int = None, setIndex : bool = True ):
      self.logStart("evalSetIndex","index: {i} delta: {d} setIndex: {s}".format( i=index, d=delta, s=setIndex ))
      newIndex = index
      
      if newIndex == None:
         if delta == None:
            self.logEnd( "delta and index are none" )
            return None
         
         newIndex = self.getIndex() + delta
      
      if not 0 <= newIndex < self._poolStringLength:
         self.logEnd( "index out of range" )
         return None
      
      if setIndex:
         self.log( "saving pool index" )
         self._poolStringIndex = newIndex
      
      self.logEnd( "returning {c}".format( c=( self._poolString[ newIndex ] ) ) )
      return self._poolString[ newIndex ]
   
   def get( self, index : int = None, setIndex : bool = False ):
      self.logStart("get","index: {i} setIndex: {s}".format( i=index, s=setIndex ))
      
      char = self.evalSetIndex( index=( index or self.getIndex() ), setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def start( self, setIndex : bool = True ):
      self.logStart("start","setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( index=0, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def end( self, setIndex : bool = True ):
      self.logStart("end","setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=( self.getCharCount() - 1 ), setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def next( self, setIndex : bool = True ):
      self.logStart("next","setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=1, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def prev( self, setIndex : bool = True ):
      self.logStart("prev","setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=-1, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def setPoolCharactersUpperCase( self ):
      self._poolString = _poolString.upper()
      return self
   
   def setPoolCharactersLowerCase( self ):
      self._poolString = _poolString.lower()
      return self

class CharPoolManager( HasState, HasStep, Log ):
   
   STATE_MOD_CAPS =    0b1
   
   STEP_STANDARD = 0
   STEP_NUMBERS = 1
   STEP_SYMBOLS = 2
   
   def __init__( self ):
      HasState.__init__( self )
      HasStep.__init__( self, CharPoolManager.STEP_STANDARD )
      Log.__init__( self, "CharPoolManager" )
      
      self._poolMap = { CharPoolManager.STEP_STANDARD : CharPool( "abcdefghijklmnopqrstuvwxyz" ),
                        CharPoolManager.STEP_NUMBERS  : CharPool( "0123456789" ),
                        CharPoolManager.STEP_SYMBOLS  : CharPool( '''!"#$%&'()*#,-./:;<=>?@[\]^_|~''' ) }
   
   def toggleStep( self, step ):
      self.logStart("toggleStep")
      if self.hasStep( step ):
         self.setStep( CharPoolManager.STEP_STANDARD )
      else:
         self.setStep( step )
      self.logEnd( str( self.getStep() ) )
   
   def _getPool( self ):
      self.logStart("_getPool step: {s}".format( s=self.getStep() ) )
      self.logEnd( "{s}".format( s=( self._poolMap.get( self.getStep() ) ) ))
      return self._poolMap.get( self.getStep() )
   
   def next( self ):
      self.logStart("next")
      newChar = self._getPool().next()
      self.logEnd("returning: {c}".format( c=newChar ))
      return newChar
   
   def prev( self ):
      self.logStart("prev")
      newChar = self._getPool().prev()
      self.logEnd("returning: {c}".format( c=newChar ))
      return newChar
   
   def getCharacter( self ):
      self.logStart("getCharacter")
      
      if self.hasState( CharPoolManager.STATE_MOD_CAPS ):
         self.logEnd("returning: {c}".format( c=( self._getPool().get().upper() ) ))
         return self._getPool().get().upper()
      
      self.logEnd("returning: {c}".format( c=( self._getPool().get() ) ))
      return self._getPool().get()
   
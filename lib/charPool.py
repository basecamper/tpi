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
      self.logStart("index: {i} delta: {d} setIndex: {s}".format( i=index, d=delta, s=setIndex ))
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
      self.logStart("index: {i} setIndex: {s}".format( i=index, s=setIndex ))
      
      char = self.evalSetIndex( index=( index or self.getIndex() ), setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def start( self, setIndex : bool = True ):
      self.logStart("setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( index=0, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def end( self, setIndex : bool = True ):
      self.logStart("setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=( self.getCharCount() - 1 ), setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def next( self, setIndex : bool = True ):
      self.logStart("setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=1, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def prev( self, setIndex : bool = True ):
      self.logStart("setIndex: {s}".format( s=setIndex ))
      
      char = self.evalSetIndex( delta=-1, setIndex=setIndex )
      
      self.logEnd("{c}".format( c=char ))
      return char
   
   def setPoolCharactersUpperCase( self ):
      self._poolString = _poolString.upper()
      return self
   
   def setPoolCharactersLowerCase( self ):
      self._poolString = _poolString.lower()
      return self

class CharPoolManager( Log ):
   
   def __init__( self ):
      
      Log.__init__( self, "CharPoolManager" )
      self._isCapsActive = False
      self._characters = CharPool( "abcdefghijklmnopqrstuvwxyz" )
      self._numbers = CharPool( "0123456789" )
      self._symbols = CharPool( '''!"#$%&'()*#,-./:;<=>?@[\]^_|~''' )
      self._activePool = self._characters
   
   def toggleCharacters( self ):
      if self._activePool != self._characters:
         self._activePool = self._characters
      else:
         self._isCapsActive = not self._isCapsActive
   
   def toggleNumbers( self ):
      if self._activePool != self._numbers:
         self._activePool = self._numbers
      else:
         self.toggleCharacters()
   
   def toggleSymbols( self ):
      if self._activePool != self._symbols:
         self._activePool = self._symbols
      else:
         self.toggleCharacters()
   
   def getCharacter( self ):
      self.logStart()
      c = self._activePool.get()
      
      if self._isCapsActive:
         c = c.upper()
         self.logEnd("returning: {c}".format( c=c ))
         return c
      
      self.logEnd("returning: {c}".format( c=c ))
      return c
   
   def next( self ):
      self.logStart()
      newChar = self._activePool.next()
      self.logEnd("returning: {c}".format( c=newChar ))
      return newChar
   
   def prev( self ):
      self.logStart()
      newChar = self._activePool.prev()
      self.logEnd("returning: {c}".format( c=newChar ))
      return newChar
   
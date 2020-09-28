from lib.log import Log
from lib.tools import EMPTY_STRING, raiseNotInstanceOf

class DictNavigator( Log ):
   def __init__( self, d : dict ):
      Log.__init__( self, "_DictNavigator" )
      
      self._dict = raiseNotInstanceOf( d, dict )
      self._currentKeyIndex = 0
      self._selectedDictPath = []
   
   def reset( self ):
      self._currentKeyIndex = 0
      self._selectedDictPath = []
   
   def _getSubDict( self ):
      sub = self._dict
      for k in self._selectedDictPath:
         sub = sub[ k ]
      return sub
   
   def _getKeyList( self ):
      return list( self._getSubDict().keys() )
   
   def _getValueList( self ):
      return list( self._getSubDict().values() )
   
   def changeKeyIndex( self, delta : int = 0 ):
      self.logStart("delta: {d}".format( d=delta ))
      newIndex = self._currentKeyIndex + delta
      if 0 <= newIndex < len( self._getSubDict() ):
         self._currentKeyIndex = newIndex
      self.logEnd("newIndex: {i}".format( i=self._currentKeyIndex ))
      return self
   
   def getValue( self ):
      self.logStart()
      v = v=self._getValueList()[ self._currentKeyIndex ]
      if isinstance( v, str ):
         self.logEnd("returning string with len: {l}".format( l=len( v ) ) )
      else:
         self.logEnd("returning subDir with len: {l}".format( l=len( v ) ) )
      
      return v
   
   def getKey( self ):
      self.logStart()
      self.logEnd("returning {k}".format( k=self._getKeyList()[ self._currentKeyIndex ] ) )
      return self._getKeyList()[ self._currentKeyIndex ]
   
   def hasStringValue( self ):
      self.logStart()
      self.logEnd("returning {b}".format( b=isinstance( self.getValue(), str ) ) )
      return isinstance( self.getValue(), str )
   
   def hasOpenedSubDict( self ):
      self.logStart()
      self.logEnd( str( bool( len( self._selectedDictPath ) > 0 ) ) )
      return bool( len( self._selectedDictPath ) > 0 )
   
   
   def getSubDictKey( self ):
      self.logStart()
      if len( self._selectedDictPath ) > 0:
         self.logEnd( "returning {k}".format( k=self._selectedDictPath[ -1 ] ) )
         return self._selectedDictPath[ -1 ]
      self.logEnd( "no subDir opened - returning emptyStr" )
      return EMPTY_STRING
   
   def openSubDict( self ):
      self.logStart()
      if not self.hasStringValue():
         self.log( "opening {k}".format( k=self.getKey() ) )
         self._selectedDictPath.append( self.getKey() )
      self.logEnd()
      return self
   
   def closeSubDict( self ):
      self.logStart()
      if len( self._selectedDictPath ) > 0:
         key = self._selectedDictPath.pop()
         self.log( "closed {k}".format( k=key ) )
         self._currentKeyIndex = list( self._getSubDict().keys() ).index( key )
      self.logEnd()
      return self
   
   def __str__( self ):
      return "key: {k} value: {v} selectedDictPath: {p}".format( k=self.getKey(), v=self.getValue(), p=self._selectedDictPath )

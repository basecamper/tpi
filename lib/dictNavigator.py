from lib.log import Log
from lib.tools import EMPTY_STRING

class DictNavigator( Log ):
   def __init__( self, d : dict ):
      Log.__init__( self, "_DictNavigator" )
      self._dict = d
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
      self.logStart("changeKeyIndex delta: {d}".format( d=delta ))
      newIndex = self._currentKeyIndex + delta
      if 0 <= newIndex < len( self._getSubDict() ):
         self._currentKeyIndex = newIndex
      self.logEnd("newIndex: {i}".format( i=self._currentKeyIndex ))
      return self
   
   def getValue( self ):
      self.logStart("getValue")
      v = v=self._getValueList()[ self._currentKeyIndex ]
      if isinstance( v, str ):
         self.logEnd("returning string with len: ".format( len( v ) ) )
      else:
         self.logEnd("returning subDir with len: ".format( len( v ) ) )
      
      return v
   
   def getKey( self ):
      self.logStart("getKey")
      self.logEnd("returning {k}".format( k=self._getKeyList()[ self._currentKeyIndex ] ) )
      return self._getKeyList()[ self._currentKeyIndex ]
   
   def hasStringValue( self ):
      self.logStart("hasStringValue")
      self.logEnd("returning {b}".format( b=isinstance( self.getValue(), str ) ) )
      return isinstance( self.getValue(), str )
   
   def hasOpenedSubDict( self ):
      self.logStart("hasOpenedSubDict")
      self.logEnd()
      return bool( len( self._selectedDictPath ) > 0 )
   
   
   def getSubDictKey( self ):
      self.logStart("getSubDictKey")
      if len( self._selectedDictPath ) > 0:
         self.logEnd( "returning {k}".format( k=self._selectedDictPath[ -1 ] ) )
         return self._selectedDictPath[ -1 ]
      self.logEnd( "no subDir opened - returning emptyStr" )
      return EMPTY_STRING
   
   def openSubDict( self ):
      self.logStart("openSubDict")
      self.logEnd()
      if not self.hasStringValue():
         self._selectedDictPath.append( self.getKey() )
      return self
   
   def closeSubDict( self ):
      self.logStart("closeSubDict")
      self.logEnd()
      if len( self._selectedDictPath ) > 0:
         k = self._selectedDictPath.pop()
         self._currentKeyIndex = list( self._getSubDict().keys() ).index( k )
      return self
   
   def __str__( self ):
      return "key: {k} value: {v} selectedDictPath: {p}".format( k=self.getKey(), v=self.getValue(), p=self._selectedDictPath )
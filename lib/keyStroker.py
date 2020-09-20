from lib.log import Log

from enum import Enum

SHIFT_KEY = chr(32)
NULL_CHAR = chr(0)

class KeyStroker( Log ):
   def __init__( self ):
      Log.__init__( self, "KeyStroker" )
      self._sending = False
      self._keyMap = {}
      self._genLoop( NULL_CHAR, 4, "abcdefghijklmnopqrstuvwxyz" )
      self._genLoop( SHIFT_KEY, 4, "ABCDEFGHIJKLMNOPQRSTUVWXYZ" )
      self._genLoop( NULL_CHAR, 30, "1234567890" )
      self._genLoop( SHIFT_KEY, 30, "!@#$%`&*()" )
      self._genKey ( NULL_CHAR, 40, "\n" )
      self._genKey ( NULL_CHAR, 43, "\t" )
      self._genKey ( NULL_CHAR, 44, " " )
      self._genLoop( NULL_CHAR, 45, "-=[]\\" )
      self._genLoop( NULL_CHAR, 51, ";'" )
      self._genLoop( NULL_CHAR, 54, ",./" )
      self._genLoop( SHIFT_KEY, 45, "_+{}|" )
      self._genLoop( SHIFT_KEY, 51, ":\"~<>?" )
      self._genKey ( NULL_CHAR, 57, "caps" )
      self._genArrayLoop ( NULL_CHAR, 58, [ "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12" ] )
      self._genArrayLoop ( NULL_CHAR, 144, [ "LANG1", "LANG2", "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8", "LANG9" ] )
      
   
   def _genReleaseKeys( self ):
      return (NULL_CHAR*8).encode()
   
   def _genKey( self, prefix, charcode : int, char : str ):
      self._keyMap[ char ] = ( prefix + NULL_CHAR + chr( charcode ) + NULL_CHAR*5 ).encode()
   
   
   def _genArrayLoop( self, prefix, startCharcode : int, strings : list ):
      counter = startCharcode
      for c in strings:
         self._genKey( prefix, counter, c )
         counter += 1
   
   def _genLoop( self, prefix, startCharcode : int, chars : str ):
      counter = startCharcode
      for c in chars:
         self._genKey( prefix, counter, c )
         counter += 1
   
   def _send( self, text : list ):
      try:
         lastChar = None
         with open( '/dev/hidg0', 'rb+' ) as fd:
            for c in text:
               if lastChar != None and lastChar == c:
                  fd.write( self._genReleaseKeys() )
               fd.write( c )
               lastChar = c
            fd.write( self._genReleaseKeys() )
      except Exception as e:
         self.logException( e, "opening /dev/hidg0" )
   
   def _parseText( self, text : str ):
      li = []
      for c in text:
         if c in self._keyMap:
            li.append( self._keyMap[ c ] )
      return li
   
   def test( self ):
      self.logStart("test")
      self.send( "\tabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n1234567890\n!@#$%^&*()\n-=[]\;'^,./\n_+{}|~:\"\n<>?\n§" )
      self.logEnd()
   
   def send( self, text : str ):
      self.logStart("send")
      if not self._sending:
         self.log("sending stringLen: {t}".format(t=len(text)))
         self._sending = True
         self._send( self._parseText( text ) )
         self._sending = False
      self.logEnd()
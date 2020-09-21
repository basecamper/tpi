from lib.log import Log
from lib.glob import GlobalRuntime, RUNTIME_CONFIG_KEY

from enum import Enum

ALT_GR_KEY = chr(64)
SHIFT_KEY = chr(32)
NULL_CHAR = chr(0)

class KEYSETTING:
   de = "de"
   en = "en"
   alpha = "alpha"

class KeyMapTools( Log ):
   
   @staticmethod
   def getKey( prefix, charcode ):
      return ( prefix + NULL_CHAR + chr( charcode ) + NULL_CHAR*5 ).encode()
   
   @staticmethod
   def genKey( keymap : dict, prefix, charcode : int, char : str ):
      keymap[ char ] = ( prefix + NULL_CHAR + chr( charcode ) + NULL_CHAR*5 ).encode()
   
   @staticmethod
   def genArrayLoop( keymap : dict, prefix, startCharcode : int, strings ):
      counter = startCharcode
      for c in strings:
         KeyMapTools.genKey( keymap, prefix, counter, c )
         counter += 1

class KeyStroker( Log ):
   def __init__( self ):
      Log.__init__( self, "KeyStroker" )
      self._sending = False
      self._keyMap_en = {}
      self._keyMap_de = {}
      self._keyMap_alpha = {}
      
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 4, "abcdefghijklmnopqrstuvwxyz" )
      KeyMapTools.genArrayLoop( self._keyMap_en, SHIFT_KEY, 4, "ABCDEFGHIJKLMNOPQRSTUVWXYZ" )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 30, "1234567890" )
      KeyMapTools.genArrayLoop( self._keyMap_en, SHIFT_KEY, 30, "!@#$%`&*()" )
      KeyMapTools.genKey      ( self._keyMap_en, NULL_CHAR, 40, "\n" )
      KeyMapTools.genKey      ( self._keyMap_en, NULL_CHAR, 43, "\t" )
      KeyMapTools.genKey      ( self._keyMap_en, NULL_CHAR, 44, " " )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 45, "-=[]\\" )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 51, ";'" )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 54, ",./" )
      KeyMapTools.genArrayLoop( self._keyMap_en, SHIFT_KEY, 45, "_+{}|" )
      KeyMapTools.genArrayLoop( self._keyMap_en, SHIFT_KEY, 51, ":\"~<>?" )
      KeyMapTools.genKey      ( self._keyMap_en, NULL_CHAR, 57, "caps" )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 58, [ "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12" ] )
      KeyMapTools.genArrayLoop( self._keyMap_en, NULL_CHAR, 144, [ "LANG1", "LANG2", "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8", "LANG9" ] )
      
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 4, "abcdefghijklmnopqrstuvwxzy" )
      KeyMapTools.genArrayLoop( self._keyMap_de, SHIFT_KEY, 4, "ABCDEFGHIJKLMNOPQRSTUVWXZY" )
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 8, "€" )
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 16, "µ" )
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 20, "@" )
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 30, "1234567890" )
      KeyMapTools.genArrayLoop( self._keyMap_de, SHIFT_KEY, 30, "!\"§$%&/()=" )
      KeyMapTools.genArrayLoop( self._keyMap_de, ALT_GR_KEY, 31, "²³" )
      KeyMapTools.genArrayLoop( self._keyMap_de, ALT_GR_KEY, 36, "{[]}" )
      KeyMapTools.genKey      ( self._keyMap_de, NULL_CHAR, 40, "\n" )
      KeyMapTools.genKey      ( self._keyMap_de, NULL_CHAR, 43, "\t" )
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 44, " ß´ü+" )
      KeyMapTools.genArrayLoop( self._keyMap_de, SHIFT_KEY, 45, "?`Ü*" )
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 51, "öä^,.-" )
      KeyMapTools.genArrayLoop( self._keyMap_de, SHIFT_KEY, 51, "ÖÄ°;:_" )
      KeyMapTools.genKey      ( self._keyMap_de, NULL_CHAR, 49, "#" )
      KeyMapTools.genKey      ( self._keyMap_de, SHIFT_KEY, 49, "'" )
      KeyMapTools.genKey      ( self._keyMap_de, SHIFT_KEY, 49, "’" ) # map special ´ to
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 45, "\\" )
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 48, "~" )
      KeyMapTools.genKey      ( self._keyMap_de, NULL_CHAR, 57, "caps" )
      KeyMapTools.genKey      ( self._keyMap_de, NULL_CHAR, 100, "<" )
      KeyMapTools.genKey      ( self._keyMap_de, SHIFT_KEY, 100, ">" )
      KeyMapTools.genKey      ( self._keyMap_de, ALT_GR_KEY, 100, "|" )
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 58, [ "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12" ] )
      KeyMapTools.genArrayLoop( self._keyMap_de, NULL_CHAR, 144, [ "LANG1", "LANG2", "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8", "LANG9" ] )
      
      
      KeyMapTools.genArrayLoop( self._keyMap_alpha, NULL_CHAR, 4, "abcdefghijklmnopqrstuvwxzy" )
      KeyMapTools.genArrayLoop( self._keyMap_alpha, SHIFT_KEY, 4, "ABCDEFGHIJKLMNOPQRSTUVWXZY" )
      KeyMapTools.genArrayLoop( self._keyMap_alpha, NULL_CHAR, 30, "1234567890" )
      
      self._nonReleaseRequired = "abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXZY1234567890"
      
      self._layouts = { KEYSETTING.de : self._keyMap_de, KEYSETTING.en : self._keyMap_en, KEYSETTING.alpha : self._keyMap_alpha };
   
   
   def _genReleaseKeys( self ):
      return (NULL_CHAR*8).encode()
   
   def _send( self, text : list ):
      try:
         lastChar = None
         for c in text:
            with open( '/dev/hidg0', 'rb+' ) as fd:
               fd.write( c )
      except Exception as e:
         self.log( "EXCEPTION" )
   
   def _parseText( self, text : str, layout : str = KEYSETTING.de ):
      self.logStart( "_parseText", "parsing {c} characters".format( c=len(text) ) )
      li = []
      kmap = self._layouts[ layout ];
      lastChar = None
      for c in text:
         if c in kmap:
            if lastChar != None and lastChar == c:
               li.append( self._genReleaseKeys() )
            li.append( kmap[ c ] )
            lastChar = c
      
      li.append( self._genReleaseKeys() )
      self.logEnd()
      return li
   
   def test( self ):
      self.logStart("test")
      li = []
      
      #counter = 4
      #for c in range(26):
      #   charCode = counter + c
      #   li += self._parseText( str(charCode) )
      #   li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      #   li.append( KeyMapTools.getKey( ALT_GR_KEY, charCode ) )
      #   li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      #   self._send( li )
      #   li = []
      
      for k in self._layouts[ KEYSETTING.de ]:
         print( k )
      
      counter = 30
      for c in range(10):
         charCode = counter + c
         li += self._parseText( str(charCode) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      
      for c in range(10):
         charCode = counter + c
         li += self._parseText( str(charCode)+"s" )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( SHIFT_KEY, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      
      for c in range(10):
         charCode = counter + c
         li += self._parseText( str(charCode)+"a" )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( ALT_GR_KEY, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      
      counter = 44
      for c in range(13):
         charCode = counter + c
         li += self._parseText( str(charCode) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      for c in range(13):
         charCode = counter + c
         li += self._parseText( str(charCode)+"s" )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( SHIFT_KEY, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      for c in range(13):
         charCode = counter + c
         li += self._parseText( str(charCode)+"a" )
         li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
         li.append( KeyMapTools.getKey( ALT_GR_KEY, charCode ) )
         li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
         self._send( li )
         li = []
      
      counter = 100
      li += self._parseText( str(counter) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      li += self._parseText( str(counter)+"s" )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( SHIFT_KEY, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      li += self._parseText( str(counter)+"a" )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( ALT_GR_KEY, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      self._send( li )
      li = []
      
      counter = 103
      li += self._parseText( str(counter) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      li += self._parseText( str(counter)+"s" )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( SHIFT_KEY, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      li += self._parseText( str(counter)+"a" )
      li.append( KeyMapTools.getKey( NULL_CHAR, 43 ) )
      li.append( KeyMapTools.getKey( ALT_GR_KEY, counter ) )
      li.append( KeyMapTools.getKey( NULL_CHAR, 40 ) )
      self._send( li )
      li = []
      
      
      self.send( "\tabcdefghijklmnopqrstuvwxyz\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n1234567890ß´\n!\"§$%&/()=?`\nöäüÖÄÜ\n,.-#;:_'\n+*~<>|\n" )
      self.logEnd()
   
   def send( self, text : str ):
      self.logStart("send")
      if not self._sending:
         self.log("sending stringLen: {t}".format(t=len(text)))
         self._sending = True
         if GlobalRuntime.hasRuntimeConfig( RUNTIME_CONFIG_KEY.keymap ):
            self._send( self._parseText( text, GlobalRuntime.getRuntimeConfig( RUNTIME_CONFIG_KEY.keymap ) ) )
         else:
            self._send( self._parseText( text ) )
         self._sending = False
      self.logEnd()

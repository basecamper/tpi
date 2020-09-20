from lib.button import Button
from lib.log import Log
from lib.keyStroker import KeyStroker
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.textConst import TEXT, COLOR
from lib.configReader import ConfigReader
from lib.dictNavigator import DictNavigator

import json

SHITTALKER_FILE = ConfigReader.getInstance().getData().get("shittalker file")

class ShitTalkerElement( ScreenElement, Log ):
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.DOWN : self.onIncreaseButtonDown,
                                              Button.UP : self.onDecreaseButtonDown } )
      Log.__init__( self, className="ShitTalkerElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[shitTalker]" )
      self._dataElement1 = ScreenElement( isEndingLine=True )
      self._keyStroker = KeyStroker()
      self._dataElement2 = ScreenElement()
      self._dict = None
      self._started = False
      
      self.addChild( self._titleElement )
      self.addChild( self._dataElement1 )
      
      self.setEnablePropagation( False )
   
   
   def loadFromFile( self, filename ):
      self.logStart( "loadFromFile" )
      try:
         with open( filename, "rb" ) as file:
            self._dict = DictNavigator( json.load( file ) )
      except Exception as e:
         self.log("Error loading {err}".format( err=e ) )
         self.logEnd()
         return False
      self.logEnd()
      return True
   
   def run( self ):
      self.logStart("run")
      if self._started:
         sendprompt = ""
         if self._dict.hasStringValue():
            sendprompt = ">>>" if self._confirmed else ">"
         
         self._dataElement1.text = "{k}{s}".format( k=self._dict.getKey(), s=sendprompt )
         self._dataElement2.text = self._dict.getSubDictKey()
      else:
         self._dataElement2.text = ">"
      
      self.logEnd()
   
   def start( self ):
      self.logStart("start")
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      self.loadFromFile( SHITTALKER_FILE )
      self._started = True
      self._confirmed = False
      self.logEnd()
   
   def end( self ):
      self.logStart("end")
      self._started = False
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      
      self.logEnd()
   
   def onOkButtonDown( self, button ):
      self.logEvent("onOkButtonDown")
      if self._started:
         pass
      self.end()
   
   def onNextButtonDown( self, button ):
      self.logEvent("onNextButtonDown")
      if not self._started:
         self.start()
      else:
         if self._dict.hasStringValue():
            if not self._confirmed:
               self._confirmed = True
            else:
               self._confirmed = False
               Log.pushStatus( "{k} sent".format( k=self._dict.getKey() ),
                               COLOR.STATUS_DEFAULT )
               self._keyStroker.send( self._dict.getValue() )
         else:
            self._dict.openSubDict()
   
   def onPrevButtonDown( self, button ):
      self.logEvent("onPrevButtonDown")
      if self._confirmed:
         self._confirmed = False
      else:
         if self._started:
            self._confirmed = False
            if self._dict.hasOpenedSubDict():
               self._dict.closeSubDict()
            else:
               self.end()
         
   def onDecreaseButtonDown( self, button ):
      self.logEvent("onDecreaseButtonDown")
      self._confirmed = False
      self._dict.changeKeyIndex( -1 )
      
   def onIncreaseButtonDown( self, button ):
      self.logEvent("onIncreaseButtonDown")
      self._confirmed = False
      self._dict.changeKeyIndex( 1 )

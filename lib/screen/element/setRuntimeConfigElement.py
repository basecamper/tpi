from lib.button import Button
from lib.log import Log
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.textConst import TEXT, COLOR
from lib.dictNavigator import DictNavigator
from lib.glob import GlobalRuntime, RUNTIME_CONFIG_KEY
from lib.keyStroker import KEYSETTING

class SetRuntimeConfigElement( ScreenElement, Log ):
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.DOWN : self.onIncreaseButtonDown,
                                              Button.UP : self.onDecreaseButtonDown } )
      Log.__init__( self, className="SetRuntimeConfigElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[cfg]" )
      self._dataElement = ScreenElement( isEndingLine=True )
      
      self._dict = DictNavigator( { RUNTIME_CONFIG_KEY.keymap : { "de" : KEYSETTING.de,
                                                                  "en" : KEYSETTING.en } } )
      self._started = False
      
      self.addChild( self._titleElement )
      self.addChild( self._dataElement )
      
      self.setEnablePropagation( False )
   
   def run( self ):
      self.logStart("run")
      if self._started:
         sendprompt = ">" if self._dict.hasStringValue() else ""
         sendprefix = ">>>" if self._confirmed else ""
      
         
         self._dataElement.text = "{p}{k}{s}".format( p=sendprefix, k=self._dict.getKey(), s=sendprompt )
      else:
         self._dataElement.text = ""
      
      self.logEnd()
   
   def start( self ):
      self.logStart("start")
      self.setExclusivePropagation( True )
      self._started = True
      self._confirmed = False
      self.logEnd()
   
   def end( self ):
      self.logStart("end")
      self._started = False
      self.setExclusivePropagation( False )
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
               Log.pushStatus( "{k} set".format( k=self._dict.getKey() ), COLOR.STATUS_DEFAULT )
               GlobalRuntime.setRuntimeConfig( self._dict.getSubDictKey(), self._dict.getValue() )
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

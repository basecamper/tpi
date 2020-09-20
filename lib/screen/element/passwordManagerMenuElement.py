from lib.button import Button
from lib.log import Log
from lib.passwordList import PasswordList
from lib.procHandler import ProcHandler
from lib.keyStroker import KeyStroker
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.textConst import TEXT, COLOR


class PasswordManagerMenuElement( ScreenElement, Log ):
   def __init__( self,
                 passwordList : object,
                 keyStroker : object ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.DOWN : self.onIncreaseButtonDown,
                                              Button.UP : self.onDecreaseButtonDown } )
      Log.__init__( self, className="PasswordManagerMenuElement" )
      
      self._passwordList = passwordList
      self._keyStroker = keyStroker
      self._accountDict = None
      self._active = False
      self._confirmed = False
      
      self._titleElement = ScreenElement( isEndingLine=True )
      self._titleElement.text, self._titleElement.color = "", Color.DEFAULT
      
      self._dataElement = ScreenElement()
      self.addChildren( [ self._titleElement, self._dataElement ] )
      
      self.setEnablePropagation( False )
      self.setButtonDownMapActive( False )
   
   def run( self ):
      self.logStart("run")
      sendprompt = ""
      if self._accountDict.hasStringValue():
         sendprompt = ">>>" if self._confirmed else ">"
      
      self._dataElement.text = "{k}{s}".format(
         k=self._accountDict.getKey(), s=sendprompt )
      
      if self._active:
         self._titleElement.text = self._accountDict.getSubDictKey()
      else:
         self._titleElement.text = ">"
      
      self.logEnd()
   
   def start( self ):
      self.logStart("start")
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      self._active = True
      self._confirmed = False
      self._accountDict = self._passwordList.getAccountDict()
      self.log( str( self._accountDict ) )
      self.logEnd()
   
   def end( self ):
      self.logStart("end")
      self._active = False
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      
      self.logEnd()
   
   def onOkButtonDown( self, button ):
      self.logEvent("onOkButtonDown")
      self.end()
   
   def onNextButtonDown( self, button ):
      self.logEvent("onNextButtonDown")
      if self._accountDict.hasStringValue():
         if not self._confirmed:
            self._confirmed = True
         else:
            self._confirmed = False
            Log.pushStatus( "{k} sent".format( k=self._accountDict.getKey() ),
                            COLOR.STATUS_DEFAULT )
            self._keyStroker.send( self._accountDict.getValue() )
      else:
         self._accountDict.openSubDict()
   
   def onPrevButtonDown( self, button ):
      self.logEvent("onPrevButtonDown")
      self._confirmed = False
      if self._accountDict.hasOpenedSubDict():
         self._accountDict.closeSubDict()
      else:
         self.end()
         
   def onDecreaseButtonDown( self, button ):
      self.logEvent("onDecreaseButtonDown")
      self._confirmed = False
      self._accountDict.changeKeyIndex( -1 )
      
   def onIncreaseButtonDown( self, button ):
      self.logEvent("onIncreaseButtonDown")
      self._confirmed = False
      self._accountDict.changeKeyIndex( 1 )

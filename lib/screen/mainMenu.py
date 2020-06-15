from lib.log import Log
from lib.button import Button
from lib.screen import ScreenElement
from lib.screen.passwordManagerElement import PasswordManagerElement

class MainMenu( ScreenElement, Log ):
   menuItems = [ PasswordManagerElement() ]
   def __init__( self,
                 buttonNext = None,
                 buttonPrev = None ):
      ScreenElement.__init__( self,
                              buttonProcMap={ buttonPrev if buttonPrev else Button.UP   : self._onPrevButtonDown,
                                              buttonNext if buttonNext else Button.DOWN : self._onNextButtonDown } )
      Log.__init__( self, "MainMenu", "buttonNext: {bn} buttonPrev: {bp}".format( bn=buttonNext, bp=buttonPrev ) )
      self._titleElement = ScreenElement( isEndingLine=True )
      self._activeElementWrapper = ScreenElement( isEndingLine=True )
      super().addChildren( [ self._titleElement, self._activeElementWrapper ] )
      
      self._activeElementIndex = 0
      
      self._activeElement = None
      
      self._setActiveElement()
   
   def _setActiveElement( self, index : int = -1 ):
      if index >= 0 and index < len( MainMenu.menuItems ):
         self._activeElementIndex = index
      
      self._activeElement = MainMenu.menuItems[self._activeElementIndex]
      self._activeElementWrapper.emptyChildren()
      self._activeElementWrapper.addChild( self._activeElement )
   
   def onButtonDown( self, button ):
      self.logStart("onButtonDown","button: {button}".format( button=button ))
      
      if self._activeElement.isExclusivePropagationRequired():
         self.log( "exclusive button callback required" )
         self._activeElement.onButtonDown( button )
      else:
         super().onButtonDown( button )
      self.logEnd()
   
   def _onNextButtonDown( self, button ):
      self.logStart("_onNextButtonDown","button: {button}".format( button=button ))
      self._setActiveElement( self._activeElementIndex + 1 )
      self.logEnd()
   
   def _onPrevButtonDown( self, button ):
      self.logStart("_onPrevButtonDown","button: {button}".format( button=button ))
      self._setActiveElement( self._activeElementIndex - 1 )
      self.logEnd()
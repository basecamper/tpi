from lib.log import Log
from lib.button import Button
from lib.screen.screenColor import Color
from lib.screen.element.passwordManagerElement import PasswordManagerElement
from lib.screen.element.simpleOsCommandElement import SimpleOsCommandElement
from lib.screen.element import ScreenElement

class MainMenu( ScreenElement, Log ):
   
   menuItems = [ PasswordManagerElement(),
                 ScreenElement( children=[ SimpleOsCommandElement( text="reboot", button=Button.RIGHT, command=["reboot"] ),
                                ScreenElement( isEndingLine=True ),ScreenElement( isEndingLine=True )
                 ]),
                 ScreenElement( children=[ SimpleOsCommandElement( text="poweroff", button=Button.RIGHT, command=["poweroff"] ),
                                ScreenElement( isEndingLine=True ),ScreenElement( isEndingLine=True )
                 ])
                  ]
   
   def __init__( self,
                 buttonNext = None,
                 buttonPrev = None ):
      ScreenElement.__init__( self )
      Log.__init__( self, "MainMenu", "buttonNext: {bn} buttonPrev: {bp}".format( bn=buttonNext, bp=buttonPrev ) )
      
      self._buttonNext = buttonNext or Button.DOWN
      self._buttonPrev = buttonPrev or Button.UP
      
      self._activeElementWrapper = ScreenElement( isEndingLine=True )
      self.addChildren( [ ScreenElement( text="---------------", isEndingLine=True, color=Color.BLACKWHITE ),
                          self._activeElementWrapper ] )
      
      self._activeElement = None
      self._activeElementIndex = 0
      self._setActiveElement()
      
      # manually forward button events to children, if required they should set exclusivePropagation which overrules this flag
      self.setEnablePropagation( False )
   
   def _getActiveElement( self ):
      return self._activeElement
   
   def _setActiveElement( self, index : int = -1 ):
      self.logStart("_setActiveElement","index: {index}".format( index=index ))
      
      if index >= 0 and index < len( MainMenu.menuItems ):
         self._activeElementIndex = index
         self.logStart("index valid")
      self._activeElement = MainMenu.menuItems[self._activeElementIndex]
      self._activeElementWrapper.emptyChildren()
      self._activeElementWrapper.addChild( self._activeElement )
      
      self.logEnd()
   
   def onButtonDown( self, button ):
      self.logStart("onButtonDown","button: {button}".format( button=button ))
      
      if button == self._buttonNext:
         self._setActiveElement( self._activeElementIndex + 1 )
      elif button == self._buttonPrev:
         self._setActiveElement( self._activeElementIndex - 1 )
      else:
         self.log("sending to: {e}".format( e=self._getActiveElement() ))
         self._getActiveElement().onButtonDown( button )
         
      self.logEnd()
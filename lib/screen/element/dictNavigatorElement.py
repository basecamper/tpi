from lib.log import Log
from lib.button import Button
from lib.screen.element import ScreenElement
from lib.dictNavigator import DictNavigator
from lib.tools import EMPTY_STRING, raiseNotInstanceOf

class DictNavigatorElement( ScreenElement, Log ):
   
   def __init__( self,
                 dictNavigator,
                 title : str,
                 onSelected ):
      
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.DOWN : self.onIncreaseButtonDown,
                                              Button.UP : self.onDecreaseButtonDown } )
      Log.__init__( self, className="DictNavigatorElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text=title )
      self._upperDataElement = ScreenElement( isEndingLine=True )
      self._lowerDataElement = ScreenElement()
      
      self._onSelected = onSelected
      self._dict = raiseNotInstanceOf( dictNavigator, DictNavigator )
      
      self._started = False
      self._selectionConfirmed = False
      
      self.addChildren( [ self._titleElement, self._upperDataElement, self._lowerDataElement ] )
      self.setEnablePropagation( False )
   
   def getDictNavigator( self ):
      return self._dict
   
   def run( self ):
      self.logStart()
      uppertext = EMPTY_STRING
      lowertext = EMPTY_STRING
      if self._started:
         sendprompt = ">" if self._dict.hasStringValue() else EMPTY_STRING
         sendprefix = ">>>" if self._selectionConfirmed else EMPTY_STRING
         
         if self._dict.hasOpenedSubDict():
            uppertext = self._dict.getSubDictKey() if self._dict.hasOpenedSubDict() else EMPTY_STRING
            lowertext = "{p}{k}{s}".format( p=sendprefix, k=self._dict.getKey(), s=sendprompt )
         else:
            uppertext = "{p}{k}{s}".format( p=sendprefix, k=self._dict.getKey(), s=sendprompt )
         
      self._upperDataElement.text = uppertext
      self._lowerDataElement.text = lowertext
      
      self.logEnd()
   
   def start( self ):
      self.logStart()
      self.setExclusivePropagation( True )
      self._started = True
      self._selectionConfirmed = False
      self.logEnd()
   
   def end( self ):
      self.logStart()
      self._dict.reset()
      self._started = False
      self.setExclusivePropagation( False )
      self.logEnd()
   
   def onOkButtonDown( self, button ):
      self.logStart()
      if self._started:
         pass
      self.end()
      self.logEnd()
   
   def onNextButtonDown( self, button ):
      self.logStart()
      if not self._started:
         self.start()
      else:
         if self._dict.hasStringValue():
            if not self._selectionConfirmed:
               self._selectionConfirmed = True
            else:
               self._selectionConfirmed = False
               self._onSelected()
         else:
            self._dict.openSubDict()
   
   def onPrevButtonDown( self, button ):
      self.logStart()
      if self._selectionConfirmed:
         self._selectionConfirmed = False
      else:
         if self._started:
            self._selectionConfirmed = False
            if self._dict.hasOpenedSubDict():
               self._dict.closeSubDict()
            else:
               self.end()
      self.logEnd()
         
   def onDecreaseButtonDown( self, button ):
      self.logStart()
      self._selectionConfirmed = False
      self._dict.changeKeyIndex( -1 )
      self.logEnd()
      
   def onIncreaseButtonDown( self, button ):
      self.logStart()
      self._selectionConfirmed = False
      self._dict.changeKeyIndex( 1 )
      self.logEnd()
   
   
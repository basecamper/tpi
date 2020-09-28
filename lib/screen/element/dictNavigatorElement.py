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
      self._dataElement = ScreenElement( isEndingLine=True )
      
      self._onSelected = onSelected
      self._dict = raiseNotInstanceOf( dictNavigator, DictNavigator )
      
      self._started = False
      self._selectionConfirmed = False
      
      self.addChildren( [ self._titleElement, self._dataElement ] )
      self.setEnablePropagation( False )
   
   def getDictNavigator( self ):
      return self._dict
   
   def run( self ):
      self.logStart()
      if self._started:
         sendprompt = ">" if self._dict.hasStringValue() else EMPTY_STRING
         sendprefix = ">>>" if self._selectionConfirmed else EMPTY_STRING
         
         self._dataElement.text = "{p}{k}{s}".format( p=sendprefix, k=self._dict.getKey(), s=sendprompt )
      else:
         self._dataElement.text = EMPTY_STRING
      
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
               self._onSelected()
               self.end()
         else:
            self._dict.openSubDict()
      self.logEnd()
   
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
   
   
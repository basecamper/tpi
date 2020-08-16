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
                                              Button.UP : self.onIncreaseButtonDown,
                                              Button.DOWN : self.onDecreaseButtonDown } )
      Log.__init__( self, className="PasswordManagerMenuElement" )
      
      self._passwordList = passwordList
      self._keyStroker = keyStroker
      self._accountMap = None
      self._currentGroup = None
      self._currentAccount = None
      
      self._dataElement = ScreenElement()
      self.addChild( self._dataElement )
      
      self.setEnablePropagation( False )
      self.setButtonDownMapActive( False )
   
   def run( self ):
      self.logStart("run")
      self._dataElement.text = self._currentGroup.getKey()
      
      self.logEnd()
   
   def start( self ):
      self.logStart("start")
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      
      self._accountMap = self._passwordList.getAccountMap()
      self.log( str( self._accountMap ) )
      for a in self._accountMap:
          self.log( str( a ) )
      self._currentGroup = iter( self._accountMap )
      self._setNextGroup()
      
      self.logEnd()
   
   def end( self ):
      self.logStart("end")
      
      self._currentMapKey = None
      
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      
      self.logEnd()
   
   def _setNextGroup( self ):
      try:
         self._currentGroup = next( self._currentGroup )
      except StopIteration:
         pass
   
   def setPrevGroup( self ):
      prevGroup, newGroup = None, None
      try:
         with iter( self._accountMap ) as i:
            while True:
               prevGroup = newGroup
               newGroup = next( i )
               if newGroup == self._currentGroup:
                  break
      except StopIteration:
         pass
      self._currentGroup = prevGroup or self._currentGroup
   
   def setPrevAccount( self ):
      prevAccount, newAccount = None, None
      try:
         with iter( self._accountMap.get( self._currentAccount ) ) as i:
            while True:
               prevAccount = newAccount
               newAccount = next( i )
               if newAccount == self._currentAccount:
                  break
      except StopIteration:
         pass
      self._currentAccount = prevAccount or self._currentAccount
   
   def onOkButtonDown( self, button ):
      self.logEvent("onOkButtonDown")
      pass
   
   def onNextButtonDown( self, button ):
      self.logEvent("onNextButtonDown")
      try:
         if self._currentAccount != None:
            self._currentAccount == None
         else:
            self.end()
      except StopIteration:
         pass
   
   def onPrevButtonDown( self, button ):
      self.logEvent("onPrevButtonDown")
      if self._currentAccount != None:
         self._currentAccount == None
      else:
         self.end()
   
   def onDecreaseButtonDown( self, button ):
      self.logEvent("onDecreaseButtonDown")
      if self._currentAccount != None:
         self.setPrevAccount()
      else:
         self.setPrevGroup()
      
   def onIncreaseButtonDown( self, button ):
      self.logEvent("onIncreaseButtonDown")
      try:
         if self._currentAccount != None:
            self._currentAccount = next( self._currentAccount )
         else:
            self._currentGroup = next( self._currentGroup )
      except StopIteration:
         pass

from lib.log import Log
from lib.button import Button
from lib.tools import EMPTY_STRING
from lib.charPool import CharPoolManager
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement

class PasswordEditElement( ScreenElement, Log ):
   
   PW_HIDDEN_CHAR = "*"
   
   def __init__( self,
                 hideUnselectedChars : bool = True ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.UP : self.onDecreaseButtonDown,
                                              Button.DOWN : self.onIncreaseButtonDown,
                                              Button.KEY1 : self.onCapsButtonDown,
                                              Button.KEY2 : self.onNumbersButtonDown,
                                              Button.KEY3 : self.onSymbolsButtonDown } )
      Log.__init__( self, className="PasswordEditElement" )
      
      
      self._charPoolManager = CharPoolManager()
      
      self._parentOnEditingFinished = None
      self._parentOnEditingCancelled = None
      self._pwTextPreElement = ScreenElement()
      self._pwTextCharElement = ScreenElement( color=Color.BLACKWHITE )
      self._pwTextPostElement = ScreenElement()
      self.addChildren( [ self._pwTextPreElement, self._pwTextCharElement, self._pwTextPostElement ] )
      
      self._pwText = ""
      self._pwTextCurrentChar = "a"
      self._pwTextCurrentCharIndex = 0
      
      self._hideUnselectedChars = hideUnselectedChars
      
      self.setButtonDownMapActive( False )
   
   def startEditing( self, onEditingFinished : object = None, onEditingCancelled : object = None ):
      self.logStart( "startEditing" )
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      self._parentOnEditingFinished = onEditingFinished
      self._parentOnEditingCancelled = onEditingCancelled
      
      if self.getCurrentCharIndex() < self.getPasswordLength():
         self._setCurrentCharFromPassword()
      else:
         self._setCurrentCharFromPool()
      
      self.logEnd()
   
   def run( self ):
      self.logStart( "run" )
      self._updatePwTextElements()
      self.logEnd()
   
   def _endEditingCancelled( self ):
      self.logStart( "_endEditingCancelled" )
      
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      if self._parentOnEditingCancelled:
         self._parentOnEditingCancelled( self._pwText )
      self.logEnd()
   
   def _endEditingFinished( self ):
      self.logStart( "_endEditingFinished" )
      if self.getCurrentCharIndex() >= self.getPasswordLength():
         self._saveCurrentChar()
      
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      if self._parentOnEditingFinished:
         self._parentOnEditingFinished( self._pwText )
      self.logEnd()
   
   def _updatePwTextElements( self ):
      self.logStart( "_updatePwTextElements" )
      char, pre, post = EMPTY_STRING, EMPTY_STRING, EMPTY_STRING
      
      if self.isEditingActive():
         slen = len( self._pwText )
         preLen = self._pwTextCurrentCharIndex
         postLen = slen - self._pwTextCurrentCharIndex - 1
         
         self.log("strLen: {slen} charIdx: {idx} preLen: {pre} postLen: {post}".format( slen=slen,
                                                                                        idx=self._pwTextCurrentCharIndex,
                                                                                        pre=preLen,
                                                                                        post=postLen ))
         
         # TODO implement self._hideUnselectedChars == False
         pre = EMPTY_STRING if preLen < 0 else PasswordEditElement.PW_HIDDEN_CHAR * preLen
         char = self._pwTextCurrentChar
         post = EMPTY_STRING if postLen < 0 else PasswordEditElement.PW_HIDDEN_CHAR * postLen

      self._pwTextPreElement.text = pre
      self._pwTextCharElement.text = char
      self._pwTextPostElement.text = post
      self.logEnd( "{pr}{ch}{po}".format( pr=pre, ch=char, po=post ) )
   
   def isEditingActive( self ):
      return self.hasExclusivePropagation()
   
   def _setCurrentChar( self, char : str ):
      self._pwTextCurrentChar = char
   
   def getCurrentCharIndex( self ):
      return self._pwTextCurrentCharIndex
   
   def getPasswordLength( self ):
      return len( self._pwText )
   
   def _clearPassword( self ):
      self._pwText = str()
   
   def _setCurrentCharFromPool( self ):
      self.logStart( "_setCurrentCharFromPool" )
      self._setCurrentChar( self._charPoolManager.getCharacter() )
      self.logEnd( self._pwTextCurrentChar )
   
   def _setCurrentCharFromPassword( self ):
      self.logStart( "_setCurrentCharFromPassword" )
      self._setCurrentChar( self._pwText[self._pwTextCurrentCharIndex] )
      self.logEnd( self._pwTextCurrentChar )
   
   def _decrementCurrentCharIndex( self ):
      self.logStart( "_decrementCurrentCharIndex" )
      
      if self._pwTextCurrentCharIndex == 0:
         self.logEnd( str(False) )
         return False
      self._pwTextCurrentCharIndex -= 1
      self._setCurrentCharFromPassword()
      
      self.logEnd( str(self._pwTextCurrentCharIndex) )
      return True
   
   def _incrementCurrentCharIndex( self ):
      self.logStart( "_incrementCurrentCharIndex" )
      
      self._saveCurrentChar()
      
      self._pwTextCurrentCharIndex += 1
      
      if self._pwTextCurrentCharIndex < self.getPasswordLength():
         self._setCurrentCharFromPassword()
      else:
         self._setCurrentCharFromPool()
      
      self.logEnd( str(self._pwTextCurrentCharIndex) )
      return True
   
   def _saveCurrentChar( self ):
      self.logStart( "_saveCurrentSelectedChar" )
      idx = self._pwTextCurrentCharIndex
      self._pwText = self._pwText[:idx] + self._pwTextCurrentChar + self._pwText[idx + 1:]
      self.logEnd()
   
   def onOkButtonDown( self, button ):
      self.logStart( "onOkButtonDown" )
      self._endEditingFinished()
      self.logEnd()
   
   def onPrevButtonDown( self, button ):
      self.logStart( "onPrevButtonDown" )
      if not self._decrementCurrentCharIndex():
         self._clearPassword()
         self._endEditingCancelled()
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def onNextButtonDown( self, button ):
      self.logStart( "onNextButtonDown" )
      self._incrementCurrentCharIndex()
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def onIncreaseButtonDown( self, button ):
      self.logStart( "onIncreaseButtonDown" )
      
      self._charPoolManager.next()
      self._setCurrentCharFromPool()
      
      self.logEnd()
      
   def onDecreaseButtonDown( self, button ):
      self.logStart( "onDecreaseButtonDown" )
      
      self._charPoolManager.prev()
      self._setCurrentCharFromPool()
      
      self.logEnd()
      
   def onCapsButtonDown( self, button ):
      self.logStart( "onCapsButtonDown" )
      self._toggleCharacters()
      self._setCurrentCharFromPool()
      self.logEnd()
      
   def onNumbersButtonDown( self, button ):
      self.logStart( "onNumbersButtonDown" )
      self._toggleNumbers()
      self._setCurrentCharFromPool()
      self.logEnd()
      
   def onSymbolsButtonDown( self, button ):
      self.logStart( "onSymbolsButtonDown" )
      self._toggleSymbols()
      self._setCurrentCharFromPool()
      self.logEnd()
   
   @staticmethod
   def getNextCharacter( currentIndex : str, list : str, steps : int = 1 ):
      nextIndex = currentIndex + steps
      if nextIndex > 0 and nextIndex < len( list ):
         return list[nextIndex]
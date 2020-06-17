from lib.log import Log
from lib.button import Button
from lib.tools import EMPTY_STRING
from lib.hasState import HasState
from lib.hasStep import HasStep
from lib.charPool import CharPoolManager
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement

class PasswordEditElement( ScreenElement, HasState, HasStep, Log ):
   
   STATE_CHAR_FROM_POOL_ACTIVE = 0b1
   
   STEP_IDLE = 0
   STEP_START = 1
   STEP_EDIT = 2
   STEP_EDIT_ABORT = 3
   STEP_EDIT_FINISHED = 4
   STEP_CLEANUP = 5
   
   PW_HIDDEN_CHAR = "*"
   
   def __init__( self, hideUnselectedChars : bool = True ):
      ScreenElement.__init__( self,
                              buttonProcMap={ Button.PRESS : self.onOkButtonDown,
                                              Button.LEFT : self.onPrevButtonDown,
                                              Button.RIGHT : self.onNextButtonDown,
                                              Button.UP : self.onIncreaseButtonDown,
                                              Button.DOWN : self.onDecreaseButtonDown,
                                              Button.KEY1 : self.onCapsButtonDown,
                                              Button.KEY2 : self.onNumbersButtonDown,
                                              Button.KEY3 : self.onSymbolsButtonDown } )
      HasState.__init__( self )
      HasStep.__init__( self, PasswordEditElement.STEP_IDLE )
      Log.__init__( self, className="PasswordEditElement" )
      
      self._charPoolManager = CharPoolManager()
      
      self._pwTextPreElement = ScreenElement()
      self._pwTextCharElement = ScreenElement( color=Color.BLACKWHITE )
      self._pwTextPostElement = ScreenElement()
      self.addChildren( [ self._pwTextPreElement, self._pwTextCharElement, self._pwTextPostElement ] )
      
      self._pwText = ""
      self._pwTextCurrentChar = "a"
      self._pwTextCurrentCharIndex = 0
      
      self._hideUnselectedChars = hideUnselectedChars
   
   def run( self ):
      self.logStart( "run" )
      if self.hasStep( PasswordEditElement.STEP_IDLE ):
         pass
      
      if self.hasStep( PasswordEditElement.STEP_START ):
         self.log( "executing STEP_START" )
         self.setExclusivePropagation( True )
         
         self.setStep( PasswordEditElement.STEP_EDIT )
      
      if self.hasStep( PasswordEditElement.STEP_EDIT ):
         self.log( "executing STEP_EDIT" )
         
         if (    self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
              or self.getCurrentCharIndex() >= self.getPasswordLength() ):
            self._initCurrentCharFromPool()
         else:
            self._initCurrentCharFromPassword()
            
         self.runPwTextElement()
      
      if self.hasStep( PasswordEditElement.STEP_EDIT_FINISHED ):
         self.log( "executing STEP_EDIT_FINISHED" )
         
         self.setStep( PasswordEditElement.STEP_CLEANUP )
      
      if self.hasStep( PasswordEditElement.STEP_EDIT_ABORT ):
         self.log( "executing STEP_EDIT_ABORT" )
         self._pwText = EMPTY_STRING
         
         self.setStep( PasswordEditElement.STEP_CLEANUP )
      
      if self.hasStep( PasswordEditElement.STEP_CLEANUP ):
         self.log( "executing STEP_CLEANUP" )
         self._pwTextCurrentCharIndex = 0
         self._pwTextPreElement.text = EMPTY_STRING
         self._pwTextCharElement.text = EMPTY_STRING
         self._pwTextPostElement.text = EMPTY_STRING
         
         self.setStep( PasswordEditElement.STEP_IDLE )
         self.setExclusivePropagation( False )
      
      self.logEnd()
   
   def runPwTextElement( self ):
      self.logStart( "runPwTextElement" )
      
      slen = len( self._pwText )
      preLen = self._pwTextCurrentCharIndex
      postLen = slen - self._pwTextCurrentCharIndex - 1
      
      self.log("strLen: {slen} charIdx: {idx} preLen: {pre} postLen: {post}".format( slen=slen,
                                                                                     idx=self._pwTextCurrentCharIndex,
                                                                                     pre=preLen,
                                                                                     post=postLen ))
      
      # TODO implement self._hideUnselectedChars == False
      self._pwTextPreElement.text = EMPTY_STRING if preLen < 0 else PasswordEditElement.PW_HIDDEN_CHAR * preLen
      self._pwTextCharElement.text = self._pwTextCurrentChar if self.isEditingActive() else EMPTY_STRING
      self._pwTextPostElement.text = EMPTY_STRING if postLen < 0 else PasswordEditElement.PW_HIDDEN_CHAR * postLen
      
      self.logEnd()
   
   def isEditingActive( self ):
      return self.hasStep( PasswordEditElement.STEP_EDIT ) or self.hasStep( PasswordEditElement.STEP_START )
   
   def _initCurrentChar( self, char : str ):
      self._pwTextCurrentChar = char
   
   def _initCurrentCharFromPool( self ):
      self.logStart( "_initCurrentCharFromPool" )
      if not self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE ):
         self.setState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
      self._initCurrentChar( self._charPoolManager.getCharacter() )
      self.logEnd( self._pwTextCurrentChar )
   
   def _initCurrentCharFromPassword( self ):
      self.logStart( "_initCurrentCharFromPassword" )
      if self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE ):
         self.delState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
      self._initCurrentChar( self._pwText[self._pwTextCurrentCharIndex] )
      self.logEnd( self._pwTextCurrentChar )
   
   def getCurrentCharIndex( self ):
      return self._pwTextCurrentCharIndex
   
   def _decrementCurrentCharIndex( self ):
      self.logStart( "_decrementCurrentCharIndex" )
      if self._pwTextCurrentCharIndex == 0:
         self.logEnd( str(False) )
         return False
      self._pwTextCurrentCharIndex -= 1
      self.logEnd( str(self._pwTextCurrentCharIndex) )
      return True
   
   def _incrementCurrentCharIndex( self ):
      self.logStart( "_incrementCurrentCharIndex" )
      self._pwTextCurrentCharIndex += 1
      self.logEnd( str(self._pwTextCurrentCharIndex) )
      return True
   
   def getPasswordLength( self ):
      return len( self._pwText )
   
   def startEditing( self ):
      self.logStart( "startEditing" )
      self.setStep( PasswordEditElement.STEP_START )
      self.logEnd()
   
   def _saveCurrentSelectedChar( self ):
      self.logStart( "_saveCurrentSelectedChar" )
      idx = self._pwTextCurrentCharIndex
      self._pwText = self._pwText[:idx] + self._pwTextCurrentChar + self._pwText[idx + 1:]
      self.logEnd()
   
   def onOkButtonDown( self, button ):
      self.logStart( "onOkButtonDown" )
       ## TODO if index == written pw.length -> write current char
      self.setStep( PasswordEditElement.STEP_EDIT_FINISHED )
      self.logEnd()
   
   def onPrevButtonDown( self, button ): ## TODO rename all callback functions to e.g. onPrevButtonDown...
      self.logStart( "onPrevButtonDown" )
      
      if self.isEditingActive():
         if self.getPasswordLength() == 0:
            self.setStep( PasswordEditElement.STEP_EDIT_ABORT )
         else:
            if self._decrementCurrentCharIndex():
               self.delState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
            else:
               self.setStep( PasswordEditElement.STEP_EDIT_ABORT )
         
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def onNextButtonDown( self, button ):
      self.logStart( "onNextButtonDown" )
      
      if self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE ):
         self._saveCurrentSelectedChar()
      self._incrementCurrentCharIndex()
      
      if self.getCurrentCharIndex() < self.getPasswordLength():
         self.delState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
      
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def onIncreaseButtonDown( self, button ):
      self.logStart( "onIncreaseButtonDown" )
      
      if not self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE ):
         self.setState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
      else:
         self._charPoolManager.next()
      
      self.logEnd()
      
   def onDecreaseButtonDown( self, button ):
      self.logStart( "onDecreaseButtonDown" )
      
      if not self.hasState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE ):
         self.setState( PasswordEditElement.STATE_CHAR_FROM_POOL_ACTIVE )
      else:
         self._charPoolManager.prev()
      
      self.logEnd()
      
   def onCapsButtonDown( self, button ):
      self.logStart( "onCapsButtonDown" )
      self._charPoolManager.toggleState( CharPoolManager.STATE_MOD_CAPS )
      self.logEnd()
      
   def onNumbersButtonDown( self, button ):
      self.logStart( "onNumbersButtonDown" )
      self._charPoolManager.toggleStep( CharPoolManager.STEP_NUMBERS )
      self.logEnd()
      
   def onSymbolsButtonDown( self, button ):
      self.logStart( "onSymbolsButtonDown" )
      self._charPoolManager.toggleStep( CharPoolManager.STEP_SYMBOLS )
      self.logEnd()
   
   @staticmethod
   def getNextCharacter( currentIndex : str, list : str, steps : int = 1 ):
      nextIndex = currentIndex + steps
      if nextIndex > 0 and nextIndex < len( list ):
         return list[nextIndex]
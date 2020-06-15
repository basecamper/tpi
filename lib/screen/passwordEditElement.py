from lib.log import Log
from lib.button import Button
from lib.tools import HasState, HasStep, EMPTY_STRING
from lib.screen import ScreenElement
from lib.screen.screenColor import Color

class PasswordEditElement( ScreenElement, HasState, HasStep, Log ):
   
   STATE_MOD_CAPS =    0b001
   STATE_MOD_NUMBERS = 0b010
   STATE_MOD_SYMBOLS = 0b100
   
   STEP_IDLE = 0
   STEP_START = 1
   STEP_EDIT = 2
   STEP_CLEANUP = 3
   
   PW_HIDDEN_CHAR = "*"
   
   def __init__( self, hideUnselectedChars : bool = True ):
      ScreenElement.__init__( self,
                              buttonProcMap={ Button.PRESS : self.okProc,
                                              Button.LEFT : self.prevProc,
                                              Button.RIGHT : self.nextProc,
                                              Button.UP : self.increaseProc,
                                              Button.DOWN : self.decreaseProc,
                                              Button.KEY1 : self.charactersCapsProc,
                                              Button.KEY2 : self.numbersProc,
                                              Button.KEY3 : self.symbolsProc } )
      HasState.__init__( self )
      HasStep.__init__( self, PasswordEditElement.STEP_IDLE )
      Log.__init__( self, className="PasswordEditElement" )
      
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
         self.runPwTextElement()
      
      if self.hasStep( PasswordEditElement.STEP_CLEANUP ):
         self.log( "executing STEP_CLEANUP" )
         self.setExclusivePropagation( False )
         self._pwTextCurrentCharIndex == 0
         self._pwTextPreElement.text = EMPTY_STRING
         self._pwTextCharElement.text = EMPTY_STRING
         self._pwTextPostElement.text = EMPTY_STRING
         self._pwText = EMPTY_STRING
         
         self.setStep( PasswordEditElement.STEP_IDLE )
      
      self.logEnd()
   
   def runPwTextElement( self ):
      self.logStart( "runPwTextElement" )
      
      slen = len( self._pwText )
      preLen = self._pwTextCurrentCharIndex
      postLen = slen - self._pwTextCurrentCharIndex - 1
      
      if preLen >= 0:
         if self._hideUnselectedChars:
            self._pwTextPreElement.text = PasswordEditElement.PW_HIDDEN_CHAR * preLen
         else:
            self._pwTextPreElement.text = self._pwText[0:preLen]
            
      
      self._pwTextCharElement.text = self._pwTextCurrentChar if self.isEditingActive() else EMPTY_STRING
      
      if postLen >= 0:
         if self._hideUnselectedChars:
            self._pwTextPostElement.text = PasswordEditElement.PW_HIDDEN_CHAR * postLen
         else:
            self._pwTextPostElement.text = self._pwText[preLen+1]
      
      self.logEnd()
   
   def isEditingActive( self ):
      return self.hasStep( PasswordEditElement.STEP_EDIT ) or self.hasStep( PasswordEditElement.STEP_START )
   
   def isPasswordValid( self ):
      self.logStart( "isPasswordValid" )
      self.logEnd("False")
      return False
   
   def startEditing( self ):
      self.logStart( "startEditing" )
      self.setStep( PasswordEditElement.STEP_START )
      self.logEnd()
   
   def _saveCurrentSelectedChar( self ):
      idx = self._pwTextCurrentCharIndex
      self._pwText = self._pwText[:idx] + self._pwTextCurrentChar + self._pwText[idx + 1:]
   
   def okProc( self, button ):
      self.logStart( "okProc" )
      self.setStep( PasswordEditElement.STEP_CLEANUP ) ## TODO VALIDATE ETC
      self.logEnd()
   
   def prevProc( self, button ):
      self.logStart( "prevProc" )
      if self.isEditingActive():
         if len( self._pwText ) > 0:
            if self._pwTextCurrentCharIndex == 0:
               self.setStep( PasswordEditElement.STEP_CLEANUP )
            else:
               self._pwTextCurrentCharIndex -= 1
               self._pwTextCurrentChar = self._pwText[self._pwTextCurrentCharIndex]
         else:
            self.setStep( PasswordEditElement.STEP_CLEANUP )
         
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def nextProc( self, button ):
      self.logStart( "nextProc" )
      self._saveCurrentSelectedChar()
      self._pwTextCurrentCharIndex += 1
      self.logEnd( "index: {i} pass: {p}".format( i=self._pwTextCurrentCharIndex, p=self._pwText ) )
      
   def increaseProc( self, button, amount : int = 1 ):
      self.logStart( "increaseProc" )
      self.logEnd()
      
   def decreaseProc( self, button, amount : int = 1 ):
      self.logStart( "decreaseProc" )
      self.logEnd()
      
   def charactersCapsProc( self ):
      self.logStart( "charactersCapsProc" )
      self.toggleState( STATE_MOD_CAPS )
      self.logEnd()
      
   def numbersProc( self ):
      self.logStart( "numbersProc" )
      self.toggleState( STATE_MOD_NUMBERS )
      self.logEnd()
      
   def symbolsProc( self ):
      self.logStart( "symbolsProc" )
      self.toggleState( STATE_MOD_SYMBOLS )
      self.logEnd()
   
   @staticmethod
   def getNextCharacter( currentIndex : str, list : str, steps : int = 1 ):
      nextIndex = currentIndex + steps
      if nextIndex > 0 and nextIndex < len( list ):
         return list[nextIndex]
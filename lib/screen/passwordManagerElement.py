import pickle

from lib.button import Button
from lib.screen import ScreenElement
from lib.log import Log
from lib.passwordList import PasswordList
from lib.procHandler import ProcHandler
from lib.hasState import HasState
from lib.hasStep import HasStep
from lib.screen.screenColor import Color
from lib.screen.passwordEditElement import PasswordEditElement

class PasswordManagerElement( ScreenElement, HasState, HasStep, Log ):
   
   STEP_START_REQUIRED = 0
   STEP_STARTED = 1
   STEP_GET_PASSWORD = 2
   STEP_INIT = 3
   STEP_SHOW_CATEGORIES = 4
   STEP_CLEANUP = 5
   
   STATE_STARTED =          0b10
   STATE_PASSWORDS_LOADED = 0b01
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonProcMap={ Button.LEFT : self.cancelProc,
                                              Button.RIGHT : self.okProc,
                                              Button.UP : self.prevProc,
                                              Button.DOWN : self.nextProc } )
      HasState.__init__( self )
      HasStep.__init__( self,
                        startStep=PasswordManagerElement.STEP_START_REQUIRED )
      Log.__init__( self, className="PasswordManagerElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[pwman]" )
      self._selectionElement = ScreenElement( isEndingLine=True )
      self._pwTextElement = PasswordEditElement()
      
      self.addChild( self._titleElement )
      self.addChild( self._selectionElement )
      self.addChild( self._pwTextElement )
      
      self.passwordList = PasswordList()
      self.setEnablePropagation( False )
      Log.pushStatus( "initialized", Color.BLACKWHITE )
   
   def run( self ):
      self.logStart( "run","step: {step}".format( step=self.getStep() ) )
      
      if self.hasStep( PasswordManagerElement.STEP_START_REQUIRED ):
         self.log( "STEP_START_REQUIRED" )
         self._selectionElement.text = "> start"
      
      if self.hasStep( PasswordManagerElement.STEP_STARTED ):
         self.log( "STEP_STARTED" )
         
         if self.hasState( PasswordManagerElement.STATE_PASSWORDS_LOADED ):
            self.log( "STATE_PASSWORDS_LOADED" )
            self.setStep( PasswordManagerElement.STEP_SHOW_CATEGORIES )
         
         else:
            self.setStep( PasswordManagerElement.STEP_GET_PASSWORD )
            self._pwTextElement.startEditing()
      
      if self.hasStep( PasswordManagerElement.STEP_GET_PASSWORD ):
         self.log( "STEP_GET_PASSWORD" )
         self._selectionElement.text = "> enter pw"
      
         if not self._pwTextElement.isEditingActive():
            self.log( "not isEditingActive" )
            # 
            # if self._pwTextElement.isPasswordValid():
            #    self.log( "isPasswordValid" )
            #    self.setStep( PasswordManagerElement.STEP_SHOW_CATEGORIES )
            #    
            # else:
            #    self.log( "not isPasswordValid" )
            self._selectionElement.text = "failed"
            Log.pushStatus( "failed", Color.RED )
            self.setStep( PasswordManagerElement.STEP_CLEANUP )
      
      if self.hasStep( PasswordManagerElement.STEP_SHOW_CATEGORIES ):
         self.log( "STEP_SHOW_CATEGORIES" )
         self._selectionElement.text = "gmx"
      
      if self.hasStep( PasswordManagerElement.STEP_CLEANUP ):
         self.log( "STEP_CLEANUP" )
         self.startStep()
      
      super().run()
      self.logEnd( "step: {step}".format( step=self.getStep() ) )
      
   def okProc( self, button ):
      self.logStart( "okProc","button {b} step {s}".format( b=button, s=self.getStep() ) )
      if self.hasStep( PasswordManagerElement.STEP_START_REQUIRED ):
         self.setStep( PasswordManagerElement.STEP_STARTED )
      self.logEnd()
   
   def cancelProc( self, button ):
      self.logStart( "cancelProc","button {b} step {s}".format( b=button, s=self.getStep() ) )
      if self.hasStep( PasswordManagerElement.STEP_GET_PASSWORD ):
         pass
      self.log( "cancelProc" )
      self.logEnd()
   
   def prevProc( self, button ):
      self.logStart( "prevProc","button {b} step {s}".format( b=button, s=self.getStep() ) )
      if self.hasStep( PasswordManagerElement.STEP_GET_PASSWORD ):
         return
      self.log( "prevProc" )
      self.logEnd()
      
   def nextProc( self, button ):
      self.logStart( "nextProc","button {b} step {s}".format( b=button, s=self.getStep() ) )
      if self.hasStep( PasswordManagerElement.STEP_GET_PASSWORD ):
         return
      self.log( "nextProc" )
      self.logEnd()


      
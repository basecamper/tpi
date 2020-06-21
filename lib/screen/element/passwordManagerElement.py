import pickle

from lib.button import Button
from lib.log import Log
from lib.passwordList import PasswordList
from lib.procHandler import ProcHandler
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.passwordEditElement import PasswordEditElement
from lib.screen.textConst import TEXT, COLOR

class PasswordManagerElement( ScreenElement, Log ):
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.LEFT : self.onCancelButtonDown,
                                              Button.RIGHT : self.onOkButtonDown } )
      Log.__init__( self, className="PasswordManagerElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[pwman]" )
      self._selectionElement = ScreenElement( isEndingLine=True )
      self._pwTextElement = PasswordEditElement()
      
      self.addChild( self._titleElement )
      self.addChild( self._selectionElement )
      self.addChild( self._pwTextElement )
      
      self._passwordList = PasswordList()
      self._editingPassword = False
      
      self.setEnablePropagation( False )
   
   def onPwEditFinished( self, password : str ):
      self.logStart( "onPwEditFinished","password {p}".format( p=password ) )
      self._passwordList.loadPasswords( password=password,
                                        onSuccess=self.onPasswordLoadSuccess,
                                        onError=self.onPasswordLoadError )
      self._editingPassword = False
      self.logEnd()
   
   def onPwEditCancelled( self, password : str ):
      self.logStart( "onPwEditCancelled","password {p}".format( p=password ) )
      self._editingPassword = False
      self.logEnd()
   
   def onPasswordLoadSuccess( self ):
      Log.pushStatus( "pws loaded", COLOR.STATUS_SUCCESS )
   
   def onPasswordLoadError( self ):
      Log.pushStatus( "ERR loading pw", COLOR.STATUS_ERROR )
   
   def onOkButtonDown( self, button ):
      self.logStart( "onOkButtonDown","button {b}".format( b=button ) )
      
      if self._passwordList.isLoaded():
         return
      else:
         if not self._editingPassword:
            self._editingPassword = True
            self._pwTextElement.startEditing( onEditingFinished=self.onPwEditFinished, onEditingCancelled=self.onPwEditCancelled )
            self._selectionElement.text, self._selectionElement.color = "main pw>", Color.DEFAULT
            Log.pushStatus( "start edit", COLOR.STATUS_DEFAULT )
      
      self.logEnd()
   
   def onCancelButtonDown( self, button ):
      self.logStart( "onCancelButtonDown","button {b}".format( b=button ) )
      self.logEnd()
   
   def onPrevButtonDown( self, button ):
      self.logStart( "onPrevButtonDown","button {b}".format( b=button ) )
      self.logEnd()
      
   def onNextButtonDown( self, button ):
      self.logStart( "onNextButtonDown","button {b}".format( b=button ) )
      self.logEnd()

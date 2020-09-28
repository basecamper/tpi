import pickle

from lib.button import Button
from lib.log import Log
from lib.passwordList import PasswordList
from lib.procHandler import ProcHandler
from lib.keyStroker import KeyStroker
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.passwordEditElement import PasswordEditElement
from lib.screen.element.passwordManagerMenuElement import PasswordManagerMenuElement
from lib.screen.textConst import TEXT, COLOR

class PasswordManagerElement( ScreenElement, Log ):
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.LEFT : self.onCancelButtonDown,
                                              Button.RIGHT : self.onOkButtonDown } )
      Log.__init__( self, className="PasswordManagerElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[pwman]" )
      
      self._passwordList = PasswordList()
      self._keyStroker = KeyStroker()
      
      self._pwTextElement = PasswordEditElement()
      self._accountMenuElement = PasswordManagerMenuElement( passwordList=self._passwordList,
                                                             keyStroker=self._keyStroker )
      self._dataWrapperElement = ScreenElement( children=[ self._pwTextElement ] )
      
      self.addChild( self._titleElement )
      self.addChild( self._dataWrapperElement )
      
      self._editingPassword = False
      
      self.setEnablePropagation( False )
      
   def passwordsLoaded( self ):
      Log.pushStatus( "pws loaded", COLOR.STATUS_SUCCESS )
      self._dataWrapperElement.emptyChildren()
      self._dataWrapperElement.addChild( self._accountMenuElement )
      self._accountMenuElement.start()
      
   def onPwEditFinished( self, password : str ):
      self.logStart( "password len {p}".format( p=len( password ) ) )
      self._passwordList.loadPasswords( password=password,
                                        onSuccess=self.onPasswordLoadSuccess,
                                        onError=self.onPasswordLoadError )
      self._editingPassword = False
      self.logEnd()
   
   def onPwEditCancelled( self, password : str ):
      self.logStart( "password len {p}".format( p=len( password ) ) )
      self._editingPassword = False
      self.logEnd()
   
   def onPasswordLoadSuccess( self ):
      self.passwordsLoaded()
   
   def onPasswordLoadError( self ):
      Log.pushStatus( "ERR loading pw", COLOR.STATUS_ERROR )
   
   def onOkButtonDown( self, button ):
      self.logStart( "button {b}".format( b=button ) )
      
      if self._passwordList.isLoaded():
         self.passwordsLoaded()
      else:
         if not self._editingPassword:
            self._editingPassword = True
            self._pwTextElement.startEditing( onEditingFinished=self.onPwEditFinished, onEditingCancelled=self.onPwEditCancelled )
            Log.pushStatus( "start edit", COLOR.STATUS_DEFAULT )
      
      self.logEnd()
   
   def onCancelButtonDown( self, button ):
      self.logStart( "button {b}".format( b=button ) )
      self.logEnd()
   
   def onPrevButtonDown( self, button ):
      self.logStart( "button {b}".format( b=button ) )
      self.logEnd()
      
   def onNextButtonDown( self, button ):
      self.logStart( "button {b}".format( b=button ) )
      self.logEnd()

import pickle

from lib.button import Button
from lib.log import Log
from lib.passwordList import PasswordList
from lib.procHandler import ProcHandler
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.passwordEditElement import PasswordEditElement
from lib.screen.textConst import TEXT, COLOR

class PasswordManagerAccount( Log ):
   def __init__( self, data : object ):
      self._data = data
   def getName( self ):
      return self._data.get("name")
   def getUser( self ):
      return self._data.get("user")
   def getMail( self ):
      return self._data.get("email")
   def getPassword( self ):
      return self._data.get("password")
   

class PasswordManagerMenuElement( ScreenElement, Log ):
   def __init__( self, passwordList : object ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.LEFT : self.onCancelButtonDown,
                                              Button.RIGHT : self.onOkButtonDown,
                                              Button.UP : self.onPrevButtonDown,
                                              Button.DOWN : self.onNextButtonDown } )
      Log.__init__( self, className="PasswordManagerMenuElement" )
      
      self._passwordList = passwordList
      self._groupSelected = False
      self._groups = []
      self._currentSelectedGroup : str = None
      self._currentSelectedAccount : str = None
      
      self._dataElement = ScreenElement()
      self.addChild( self._dataElement )
      
      self.setEnablePropagation( False )
      self.setButtonDownMapActive( False )
   
   def run( self ):
      if not self._groupSelected:
         self._dataElement.text = self._currentSelectedGroup or ""
      else:
         pass
   
   def start( self ):
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      for g in self._passwordList.getGroups():
         self._groups.append( g )
         for a in self._passwordList.getAccounts( g ):
            self._accounts.append( PasswordManagerAccount( data=a ) )
   
   def end( self ):
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
   
   def onOkButtonDown( self, button ):
      pass
   def onCancelButtonDown( self, button ):
      pass
   def onNextButtonDown( self, button ):
      pass
   def onPrevButtonDown( self, button ):
      pass

class PasswordManagerElement( ScreenElement, Log ):
   
   def __init__( self ):
      ScreenElement.__init__( self,
                              buttonDownMap={ Button.LEFT : self.onCancelButtonDown,
                                              Button.RIGHT : self.onOkButtonDown } )
      Log.__init__( self, className="PasswordManagerElement" )
      
      self._titleElement = ScreenElement( isEndingLine=True, text="[pwman]" )
      self._selectionElement = ScreenElement( isEndingLine=True )
      
      self._passwordList = PasswordList()
      self._pwTextElement = PasswordEditElement()
      self._accountMenuElement = PasswordManagerMenuElement( passwordList=self._passwordList )
      
      self.addChild( self._titleElement )
      self.addChild( self._selectionElement )
      self.addChild( self._pwTextElement )
      
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
      self.emptyChildren()
      self.addChild( self._accountMenuElement )
      self._accountMenuElement.start()
   
   def onPasswordLoadError( self ):
      Log.pushStatus( "ERR loading pw", COLOR.STATUS_ERROR )
   
   def onOkButtonDown( self, button ):
      self.logStart( "onOkButtonDown","button {b}".format( b=button ) )
      
      if self._passwordList.isLoaded():
         self._accountMenuElement.start()
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

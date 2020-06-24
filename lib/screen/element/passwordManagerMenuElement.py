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
      self._groupSelected = False
      self._accountSelected = False
      self._dataKeySelected = False
      self._currentSelectedGroup : str = None
      self._currentSelectedAccount : str = None
      self._currentSelectedAccountDataKey : str = None
      
      self._dataElement = ScreenElement()
      self.addChild( self._dataElement )
      
      self.setEnablePropagation( False )
      self.setButtonDownMapActive( False )
   
   def run( self ):
      self.logStart("run")
      if not self._groupSelected:
         self._dataElement.text = self._currentSelectedGroup or ""
      elif not self._accountSelected:
         self._dataElement.text = self._currentSelectedAccount or ""
      else:
         self._dataElement.text = self._currentSelectedAccountDataKey or ""
      
      self.logEnd()
   
   def start( self ):
      self.logStart("start")
      self.setExclusivePropagation( True )
      self.setButtonDownMapActive( True )
      self.logEnd()
   
   def end( self ):
      self.logStart("end")
      self._currentSelectedAccountDataKey = None
      self.setAccountSelected( False )
      self.setGroupSelected( False )
      self.setDataKeySelected( False )
      self.setExclusivePropagation( False )
      self.setButtonDownMapActive( False )
      self.logEnd()
   
   def setDataKeySelected( self, state : bool ):
      self.logStart("setGroupSelected","state {s}".format( s=state ))
      change = ( not ( self._dataKeySelected == state )
                 and ( not state or ( self._currentSelectedAccountDataKey != None ) ) )
      if change:
         self._dataKeySelected = state
         self._currentSelectedAccountDataKey = None if not state else self._currentSelectedAccountDataKey
      self.logEnd("return changed {c}".format( c=change ))
      return change
   
   def setGroupSelected( self, state : bool ):
      self.logStart("setGroupSelected","state {s}".format( s=state ))
      change = ( not ( self._groupSelected == state )
                 and ( not state or ( self._currentSelectedGroup != None ) ) )
      if change:
         self._groupSelected = state
         self._currentSelectedGroup = None if not state else self._currentSelectedGroup
      self.logEnd("return changed {c}".format( c=change ))
      return change
      
   def setAccountSelected( self, state : bool ):
      self.logStart("setAccountSelected","state {s}".format( s=state ))
      change = ( not ( self._accountSelected == state )
                 and ( not state or ( self._currentSelectedAccount != None ) ) )
      if change:
         self._accountSelected = state
         self._currentSelectedAccount = None if not state else self._currentSelectedAccount
      self.logEnd("return changed {c}".format( c=change ))
      return change
   
   def onOkButtonDown( self, button ):
      self.logEvent("onOkButtonDown")
      if self._groupSelected and self._accountSelected:
         self.log( "sending password", logMethod=False )
         self._keyStroker.sendCharacters(
            self._passwordList.getAccountDataValue(
               self._currentSelectedGroup,
               self._currentSelectedAccount,
               "password" )
         )
         self.end()
   
   def onNextButtonDown( self, button ):
      self.logEvent("onNextButtonDown")
      if not self._groupSelected:
         if self._currentSelectedGroup != None:
            self.log( "selecting group", logMethod=False )
            self.setGroupSelected( True )
      elif not self._accountSelected:
         if self._currentSelectedAccount != None:
            self.log( "selecting account", logMethod=False )
            self.setAccountSelected( True )
      elif not self._dataKeySelected:
         if self._currentSelectedAccountDataKey != None:
            self.log( "selecting account", logMethod=False )
            self.setDataKeySelected( True )
   
   def onPrevButtonDown( self, button ):
      self.logEvent("onCancelButtonDown")
      if self.setAccountSelected( False ):
         self.log( "selected account set to false", logMethod=False )
      elif self.setGroupSelected( False ):
         self.log( "selected group set to false", logMethod=False )
      elif self.setDataKeySelected( False ):
         self.log( "selected dataKey set to false", logMethod=False )
      else:
         self.end()
   
   def onDecreaseButtonDown( self, button ):
      self.logEvent("onDecreaseButtonDown")
      if not self._groupSelected:
         self.log( "setting next group", logMethod=False )
         self._currentSelectedGroup = self._passwordList.getNextGroup( self._currentSelectedGroup )
      elif not self._accountSelected:
         self.log( "setting next account", logMethod=False )
         self._currentSelectedAccount = self._passwordList.getNextAccount(
            self._currentSelectedGroup,
            self._currentSelectedAccount )
      else:
         self._currentSelectedAccountDataKey = self._passwordList.getNextAccountDataKey( 
            self._currentSelectedAccountDataKey,
            self._currentSelectedGroup,
            self._currentSelectedAccount )
   
   def onIncreaseButtonDown( self, button ):
      self.logEvent("onIncreaseButtonDown")
      if self._groupSelected:
         self.log( "setting prev group", logMethod=False )
         self._currentSelectedGroup = self._passwordList.getPrevGroup( self._currentSelectedGroup )
      elif self._accountSelected:
         self.log( "setting prev account", logMethod=False )
         self._currentSelectedAccount = self._passwordList.getPrevAccount(
            self._currentSelectedGroup,
            self._currentSelectedAccount )
      else:
         self._currentSelectedAccountDataKey = self._passwordList.getPrevAccountDataKey(
            self._currentSelectedAccountDataKey,
            self._currentSelectedGroup,
            self._currentSelectedAccount )
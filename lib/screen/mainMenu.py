from lib.log import Log
from lib.button import Button
from lib.screen.textConst import TEXT, COLOR
from lib.screen.element.dictNavigatorElement import DictNavigatorElement
from lib.screen.element.passwordManagerElement import PasswordManagerElement
from lib.screen.element.simpleOsCommandElement import SimpleOsCommandElement
from lib.screen.element import ScreenElement
from lib.dictNavigator import DictNavigator
from lib.glob import GlobalRuntime, RUNTIME_CONFIG_KEY
from lib.configReader import ConfigReader
from lib.keyStroker import KeyStroker, KEYSETTING
from lib.procHandler import ProcHandler
from lib.tools import EMPTY_STRING

import json

KEY_DHCPCD="dhcpcd"
KEY_WPA_SUPPLICANT="wpa_supplicant"

VALUE_POWEROFF="poweroff"
VALUE_REBOOT="reboot"
VALUE_WPA_SUPPLICANT_START="start"
VALUE_WPA_SUPPLICANT_STOP="stop"
VALUE_WPA_SUPPLICANT_STATUS="status"
VALUE_DHCPCD_START="start"
VALUE_DHCPCD_STOP="stop"
VALUE_DHCPCD_STATUS="status"

procMap = {
   VALUE_POWEROFF : ["poweroff"],
   VALUE_REBOOT : ["poweroff"],
   VALUE_WPA_SUPPLICANT_START : ["systemctl","start","wpa_supplicant@wlan0.service"],
   VALUE_WPA_SUPPLICANT_STOP : ["systemctl","stop","wpa_supplicant@wlan0.service"],
   VALUE_WPA_SUPPLICANT_STATUS : ["systemctl","status","wpa_supplicant@wlan0.service"],
   VALUE_DHCPCD_START : ["systemctl","start","dhcpcd.service"],
   VALUE_DHCPCD_STOP : ["systemctl","stop","dhcpcd.service"],
   VALUE_DHCPCD_STATUS : ["systemctl","status","dhcpcd.service"]
}

SHITTALKER_FILE = ConfigReader.getInstance().getData().get("shittalker file")

class MainMenu( ScreenElement, Log ):
   
   _runtimeConfigDict = DictNavigator(
         {  RUNTIME_CONFIG_KEY.keymap : { "de" : KEYSETTING.de,
                                          "en" : KEYSETTING.en } } )
   _sysCmdDict = DictNavigator(
         {  "poweroff" : VALUE_POWEROFF,
            "reboot" : VALUE_REBOOT,
            "dhcpcd" : { "start" : VALUE_WPA_SUPPLICANT_START,
                         "stop" : VALUE_WPA_SUPPLICANT_STOP,
                         "status" : VALUE_WPA_SUPPLICANT_STATUS },
            "wpa_supplicant" : { "start" : VALUE_DHCPCD_START,
                                 "stop" : VALUE_DHCPCD_STOP,
                                 "status" : VALUE_DHCPCD_STATUS } } )
   _shitTalkerDict = None
   
   def __init__( self,
                 buttonNext = None,
                 buttonPrev = None ):
      ScreenElement.__init__( self )
      Log.__init__( self, "MainMenu" )
      self.log( "buttonNext: {bn} buttonPrev: {bp}".format( bn=buttonNext, bp=buttonPrev ) )
      
      self._buttonNext = buttonNext or Button.DOWN
      self._buttonPrev = buttonPrev or Button.UP
      
      self._keyStroker = KeyStroker()
      self._sysCmdProc = None
      self._sysCmdTempDictName = None
      self._sysCmdTempKeyName = None
      
      self.menuItems = []
      self.menuItems.append( PasswordManagerElement() )
      
      try:
         with open( SHITTALKER_FILE, "rb" ) as file:
            MainMenu._shitTalkerDict = DictNavigator( json.load( file ) )
         
         self.menuItems.append(
               DictNavigatorElement(
                     dictNavigator=MainMenu._shitTalkerDict,
                     title="[shittalker]",
                     onSelected=self._onShitTalkerSelected
                  ) )
      except Exception as e:
         self.log("Error loading {err}".format( err=e ) )
      
      self.menuItems.append(
            DictNavigatorElement(
                  dictNavigator=MainMenu._runtimeConfigDict,
                  title="[cfg]",
                  onSelected=self._onRuntimeConfigSelected
               ))
      
      self.menuItems.append(
            DictNavigatorElement(
                  dictNavigator=MainMenu._sysCmdDict,
                  title="[cmd]",
                  onSelected=self._onSysCmdSelected
               ))
      
      self.menuItems.append(
            ScreenElement(
                  children=[
                        SimpleOsCommandElement( text="wpa_supplicant", button=Button.RIGHT, command=["systemctl","start","wpa_supplicant"] ),
                        ScreenElement( isEndingLine=True ),
                        ScreenElement( isEndingLine=True )
                     ]))
      
      self.menuItems.append(
            ScreenElement(
                  children=[
                        SimpleOsCommandElement( text="reboot", button=Button.RIGHT, command=["reboot"] ),
                        ScreenElement( isEndingLine=True ),
                        ScreenElement( isEndingLine=True )
                     ]))
      
      self.menuItems.append(
            ScreenElement(
                  children=[
                        SimpleOsCommandElement( text="poweroff", button=Button.RIGHT, command=["poweroff"] ),
                        ScreenElement( isEndingLine=True ),
                        ScreenElement( isEndingLine=True )
                     ]))
      
      self._activeElementWrapper = ScreenElement( isEndingLine=True )
      self.addChildren( [ ScreenElement( text="---------------", isEndingLine=True, color=COLOR.BORDER ),
                          self._activeElementWrapper ] )
      
      self._activeElement = None
      self._activeElementIndex = 0
      self._setActiveElement()
      
      self.setEnablePropagation( False )
   
   def _onSysCmdError( self ):
      d = MainMenu._sysCmdDict
      self.log()
      Log.pushStatus( "{s}{k}".format(
                  s="{sd}: ".format( sd=self._sysCmdTempDictName ) if self._sysCmdTempDictName else EMPTY_STRING,
                  k=self._sysCmdTempKeyName ),
            COLOR.STATUS_ERROR )
      self._sysCmdTempDictName = None
      self._sysCmdTempKeyName = None
      del self._sysCmdProc
      self._sysCmdProc = None
   
   def _onSysCmdSuccess( self ):
      d = MainMenu._sysCmdDict
      self.log()
      Log.pushStatus( "{s}{k}".format(
                  s="{sd}: ".format( sd=self._sysCmdTempDictName ) if self._sysCmdTempDictName else EMPTY_STRING,
                  k=self._sysCmdTempKeyName ),
            COLOR.STATUS_SUCCESS )
      self._sysCmdTempDictName = None
      self._sysCmdTempKeyName = None
      del self._sysCmdProc
      self._sysCmdProc = None
   
   def _onSysCmdSelected( self ):
      if not self._sysCmdProc:
         d = MainMenu._sysCmdDict
         v = d.getValue()
         cmd = procMap[ v ]
         self._sysCmdTempDictName = d.getSubDictKey() if d.hasOpenedSubDict() else None
         self._sysCmdTempKeyName = d.getValue()
         self._sysCmdProc = ProcHandler( command=cmd, onError=self._onSysCmdError, onSuccess=self._onSysCmdSuccess, timeout=5 )
         self._sysCmdProc.run()
   
   def _onRuntimeConfigSelected( self ):
      self.logStart()
      d = MainMenu._runtimeConfigDict
      GlobalRuntime.setRuntimeConfig( d.getSubDictKey(), d.getValue() )
      self.log( "set {k}: {v}".format( k=d.getSubDictKey(), v=d.getValue() ) )
      Log.pushStatus( "set {k}: {v}".format( k=d.getSubDictKey(), v=d.getValue() ), COLOR.STATUS_DEFAULT )
      self.logEnd()
   
   def _onShitTalkerSelected( self ):
      self.logStart()
      d = MainMenu._shitTalkerDict
      self._keyStroker.send( d.getValue() )
      self.log( "sent: {k}".format( k=d.getKey() ) )
      Log.pushStatus( "sent: {k}".format( k=d.getKey() ), COLOR.STATUS_DEFAULT )
      self.logEnd()
      
   
   def _getActiveElement( self ):
      return self._activeElement
   
   def _setActiveElement( self, index : int = -1 ):
      self.logStart("index: {index}".format( index=index ))
      
      if index >= 0 and index < len( self.menuItems ):
         self._activeElementIndex = index
         self.logStart("index valid")
      
      self._activeElement = self.menuItems[self._activeElementIndex]
      self._activeElementWrapper.emptyChildren()
      self._activeElementWrapper.addChild( self._activeElement )
      
      self.logEnd()
   
   def onButtonDown( self, button ):
      self.logStart("button: {button}".format( button=button ))
      
      if button == self._buttonNext:
         self._setActiveElement( self._activeElementIndex + 1 )
         
      elif button == self._buttonPrev:
         self._setActiveElement( self._activeElementIndex - 1 )
         
      else:
         self.log("sending to: {e}".format( e=self._getActiveElement() ))
         self._getActiveElement().onButtonDown( button )
         
      self.logEnd()

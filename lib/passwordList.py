from collections import OrderedDict

from lib.log import Log
from lib.button import Button
from lib.tools import getNextDictionaryItem, getPrevDictionaryItem
from lib.procHandler import ProcHandler, ProcHandlerChain
from lib.configReader import ConfigReader
from lib.screen.textConst import TEXT, COLOR
from lib.dictNavigator import DictNavigator
# import pickle
import json

_configReaderData = ConfigReader.getInstance().getData()

CRYPTED_FILE =        _configReaderData.get("crypted file")
CRYPT_DEVICE =        _configReaderData.get("crypt device")
CRYPT_DEVICE_PATH =   _configReaderData.get("crypt device path")
DECRYPTED_MOUNT_DIR = _configReaderData.get("decrypted mount dir")
PASSWORDS_FILE_NAME = _configReaderData.get("passwords file name")   

MOUNT_STATUS_HANDLER = ProcHandler( command=[ "mountpoint", DECRYPTED_MOUNT_DIR ] )
CRYPT_CLOSE_HANDLER =  ProcHandler( command=[ "cryptsetup", "close", CRYPT_DEVICE ] )
MOUNT_HANDLER =        ProcHandler( command=[ "mount", "{d}{f}".format( d=CRYPT_DEVICE_PATH, f=CRYPT_DEVICE), DECRYPTED_MOUNT_DIR ] )
UMOUNT_HANDLER =       ProcHandler( command=[ "umount", DECRYPTED_MOUNT_DIR ] )

def _getOpenCryptDeviceHandler( password : str ):
   return ProcHandler( command=[ "cryptsetup", "open", CRYPTED_FILE, CRYPT_DEVICE, "-d", "-" ],
                       stdin=password,
                       timeout=10 )

class _PasswordGenerator():
   @staticmethod
   def get( self ):
      return "test"

class _AccountDictLoader( Log ):
   def __init__( self ):
      Log.__init__( self, "_AccountDictLoader" )
      self._dict = None
   
   def getDict( self ):
      return self._dict
   
   def isLoaded( self ):
      self.log( "isLoaded {s}".format( s=( self._dict != None ) ) )
      return self._dict != None
   
   def loadFromFile( self, filename ):
      self.logStart()
      try:
         with open( filename, "rb" ) as file:
            self._dict = DictNavigator( json.load( file ) )
            self.log( "datatype {t}".format( t=type( self._dict )))
            # self._dict = OrderedDict( pickle.load( file ) )
      except Exception as e:
         self.log("Error loading {err}".format( err=e ) )
         self.logEnd()
         return False
      self.logEnd()
      return True
   
   # TODO
   #def saveToFile( self, filename ):
   #   self.logStart( "_saveToFile" )
   #   try:
   #      with open( filename, "wb" ) as file:
   #         pickle.dump( self._dict, file, pickle.HIGHEST_PROTOCOL )
   #   except Exception as e:
   #      self.logError("writing")
   #      return False
   #   self.logEnd()
   #   return True

class PasswordList( Log ):
   
   def __init__( self ):
      Log.__init__( self, "PasswordList" )
      
      self._accountDictLoader = _AccountDictLoader()
      self._openChain = None
      
      self._evalMountedHandler = ProcHandler( command=[ "mountpoint", DECRYPTED_MOUNT_DIR ] )
      
      self._closeChain = ProcHandlerChain( procHandlerChain=[ UMOUNT_HANDLER,
                                                              CRYPT_CLOSE_HANDLER ] )
      
      self._umountChain = ProcHandlerChain( procHandlerChain=[ UMOUNT_HANDLER ] )
      
      self._cryptCloseHandler = ProcHandlerChain( procHandlerChain=[ CRYPT_CLOSE_HANDLER ]  )
      
      self._evalMountedHandler.run( onSuccess=self._onInitialEvalMountedSuccess )
      
      self._parentOnSuccess = None
      self._parentOnError = None
   
   def getAccountDict( self ):
      return self._accountDictLoader.getDict()
   
   def isLoaded( self ):
      return self._accountDictLoader.isLoaded()
   
   def loadPasswords( self, password : str, onSuccess : object, onError : object ):
      self.logStart()
      
      if not self.isLoaded():
         Log.pushStatus( "opening", COLOR.STATUS_SUCCESS )
         self._parentOnSuccess = onSuccess
         self._parentOnError = onError
         
         self._openChain = ProcHandlerChain(
            procHandlerChain=[ _getOpenCryptDeviceHandler( password ), MOUNT_HANDLER ]
            )
            
         self._openChain.run( onSuccess=self._onSuccessOpenLoad,
                              onError=self._onError )
      self.logEnd()
   
   def savePasswords( self, password : str, onSuccess : object, onError : object ):
      self.logStart()
      Log.pushStatus( "opening", COLOR.STATUS_SUCCESS )
      self._parentOnSuccess = onSuccess
      self._parentOnError = onError
      
      self._openChain = ProcHandlerChain(
         procHandlerChain=[ _getOpenCryptDeviceHandler( password ),
                            MOUNT_HANDLER ]
         )
         
      self._openChain.run( onSuccess=self._onSuccessOpenSave, onError=self._onError )
      self.logEnd()
   
   def _onInitialEvalMountedSuccess( self ):
      self.log( "passwords already mounted, loading.." )
      self._accountDictLoader.loadFromFile( "{d}/{f}".format( d=DECRYPTED_MOUNT_DIR, f=PASSWORDS_FILE_NAME ) )
      
   
   def _onSuccessOpenLoad( self ):
      self.logStart()
      Log.pushStatus( "opened", COLOR.STATUS_SUCCESS )
      self._accountDictLoader.loadFromFile( "{d}/{f}".format( d=DECRYPTED_MOUNT_DIR, f=PASSWORDS_FILE_NAME ) )
      Log.pushStatus( "loaded", COLOR.STATUS_SUCCESS )
      self._closeChain.run( onSuccess=self._onSuccessClose,
                              onError=self._onError )
      self.logEnd()
   
   def _onSuccessOpenSave( self ):
      self.logStart()
      Log.pushStatus( "opened", COLOR.STATUS_SUCCESS )
      self._accountDictLoader.saveToFile( "{d}/{f}".format( d=DECRYPTED_MOUNT_DIR, f=PASSWORDS_FILE_NAME ) )
      Log.pushStatus( "saved", COLOR.STATUS_SUCCESS )
      self._closeChain.run( onSuccess=self._onSuccessClose,
                              onError=self._onError )
      self.logEnd()
   
   def _onSuccessClose( self ):
      self.logStart()
      Log.pushStatus( "closed", COLOR.STATUS_SUCCESS )
      self._parentOnSuccess()
      self.logEnd()
   
   def _onError( self ):
      self.logStart()
      Log.pushStatus( "error", COLOR.STATUS_ERROR )
      self._umountChain.run( onSuccess=self._onErrorUnmounted,
                             onError=self._onErrorUnmounted )
      self.logEnd()
   
   def _onErrorUnmounted( self ):
      self.logStart()
      self._cryptCloseHandler.run( onSuccess=self._onErrorCryptClosed,
                                   onError=self._onErrorCryptClosed )
      self.logEnd()
   
   def _onErrorCryptClosed( self ):
      self.logStart()
      self._parentOnError()
      self.logEnd()
   
   def __del__( self ):
      self._clean()
      del( self )
   
   def _clean( self ):
      self._onError()

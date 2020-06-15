from lib.log import Log
from lib.button import Button
from lib.procHandler import ProcHandler
from lib.tools import HasState, HasStep
from lib.screen import ScreenElement

class PasswordList( HasState, HasStep, Log ):

   STATE_BUSY  =                    0b100
   STATE_MOUNTED =                  0b010
   STATE_CRYPT_OPENED =             0b001
   
   STEP_INIT = 0
   STEP_IDLE = 1
   STEP_LOAD_PASSWORDS = 2
   STEP_POST_LOADING = 3
   STEP_SAVE_PASSWORDS = 4
   STEP_POST_SAVING = 5
   STEP_CLEANUP = 9

   CRYPT_DIR = "./mnt"
   CRYPTED_FILE = "./pws.bin"
   SERIALIZED_DICT = "./mnt/pws.bin"
   
   CRYPT_DEVICE = "passwords"
   CRYPT_DEVICE_PATH = "/dev/mapper/passwords"
   
   def __init__( self ):
      HasState.__init__( self )
      HasStep.__init__( self, PasswordList.STEP_INIT )
      Log.__init__( self, "PasswordList" )
      self._map = {}
      
      self.mountedStatusProc = ProcHandler(     command=[   "mountpoint",
                                                            PasswordList.CRYPT_DIR ],
                                                fullCallback=self._procMountStatus )
      self.cryptDeviceStatusProc = ProcHandler( command=[   "[ -e {file}]".format( file=PasswordList.CRYPT_DEVICE_PATH ) ],
                                                fullCallback=self._procCryptDeviceStatus )
      self.cryptOpenProc = ProcHandler(         command=[   "cryptsetup",
                                                            "open",
                                                            PasswordList.CRYPT_DEVICE ],
                                                fullCallback=self._procCryptOpen )
      self.cryptCloseProc = ProcHandler(        command=[   "cryptsetup",
                                                            "close",
                                                            PasswordList.CRYPT_DEVICE ],
                                                fullCallback=self._procCryptClose )
      self.mountCryptDirProc = ProcHandler(     command=[   "mount",
                                                            PasswordList.CRYPT_DEVICE_PATH,
                                                            PasswordList.CRYPT_DIR ],
                                                fullCallback=self._procMount )
      self.unmountCryptDirProc = ProcHandler(   command=[   "umount",
                                                            PasswordList.CRYPT_DIR ],
                                                fullCallback=self._procUmount )
   
   
   def __del__( self ):
      self._clean()
      del( self )
   
   def _clean( self ): pass ## TODO panic
   
   def run( self ):
      self.logStart( "run","step {s}".format( s=self.getStep() ) )
      if not self.hasState( PasswordList.STATE_BUSY ):
         
         # step init
         if self.hasStep( PasswordList.STEP_INIT ):
            # do stuff
            self.setStep( PasswordList.STEP_IDLE )
         
         # step idle
         if self.hasStep( PasswordList.STEP_IDLE ): return
         
         # step load
         if self.hasStep( PasswordList.STEP_LOAD_PASSWORDS ):
            
            if not self.hasState( PasswordList.STATE_CRYPT_OPENED ):
               self._executeProc( self.cryptOpenProc.run )
            
            elif not self.hasState( PasswordList.STATE_MOUNTED ):
               self._executeProc( self.mountCryptDirProc.run )
            
            else:
               self._loadFromFile()
               self.setStep( PasswordList.STEP_POST_LOADING )
         
         # step post load
         if hasStep( PasswordList.STEP_POST_LOADING ):
            
            if self.hasState( PasswordList.STATE_MOUNTED ):
               self._executeProc( self.unmountCryptDirProc.run )
            
            elif self.hasState( PasswordList.STATE_CRYPT_OPENED ):
               self._executeProc( self.cryptCloseProc.run )
            
            else:
               self.setStep( PasswordList.STEP_CLEANUP )
         
         # step save
         if self.hasStep( PasswordList.STEP_SAVE_PASSWORDS ):
            
            if not self.hasState( PasswordList.STATE_CRYPT_OPENED ):
               self._executeProc( self.cryptOpenProc.run )
            
            elif not self.hasState( PasswordList.STATE_MOUNTED ):
               self._executeProc( self.mountCryptDirProc.run )
            
            else:
               self._saveToFile()
               self.setStep( PasswordList.STEP_POST_SAVING )
         
         # step post save
         if hasStep( PasswordList.STEP_POST_SAVING ):
            
            if self.hasState( PasswordList.STATE_MOUNTED ):
               self._executeProc( self.unmountCryptDirProc.run )
            
            elif self.hasState( PasswordList.STATE_CRYPT_OPENED ):
               self._executeProc( self.cryptCloseProc.run )
            
            else:
               self.setStep( PasswordList.STEP_CLEANUP )
         
         # step cleanup
         if hasStep( PasswordList.STEP_CLEANUP ):
            self._state = 0
            self.setStep( PasswordList.STEP_INIT )
      
      self.logEnd()
   
   def _executeProc( self, func ):
      self.logStart( "_executeProc" )
      self._preProc( func )
      func()
      self.logEnd()
   
   def _preProc( self, func ):
      self.logStart( "_preProc" )
      self.setState( PasswordList.STATE_BUSY )
      self.logEnd()
   
   def _postProc( self, process ):
      self.logStart( "_postProc" )
      self.delState( PasswordList.STATE_BUSY )
      self.logEnd()
   
   def _procMountStatus( self, process ): # TODO unused, implement during init
      self.logStart( "_procMountStatus" )
      self._preProc( process )
      if process.returnvalue == 0:
         self.setState( PasswordList.STATE_MOUNTED )
      else:
         self.delState( PasswordList.STATE_MOUNTED )
      self._postProc( process )
      self.logEnd()
   
   def _procCryptDeviceStatus( self, process ): # TODO unused, implement during init
      self.logStart( "_procCryptDeviceStatus" )
      if process.returnvalue == 0:
         self.setState( PasswordList.STATE_CRYPT_OPENED )
      else:
         self.delState( PasswordList.STATE_CRYPT_OPENED )
      self._postProc( process )
      self.logEnd()
   
   def _procCryptOpen( self, process ):
      self.logStart( "_procCryptOpen" )
      if process.returnvalue == 0:
         self.setState( PasswordList.STATE_CRYPT_OPENED )
      self._postProc( process )
      self.logEnd()
   
   def _procCryptClose( self, process ):
      self.logStart( "_procCryptClose" )
      if process.returnvalue == 0:
         self.delState( PasswordList.STATE_CRYPT_OPENED )
      self._postProc( process )
      self.logEnd()
   
   def _procMount( self, process ):
      self.logStart( "_procMount" )
      if process.returnvalue == 0:
         self.setState( PasswordList.STATE_MOUNTED )
      self._postProc( process )
      self.logEnd()
   
   def _procUmount( self, process ):
      self.logStart( "_procUmount" )
      if process.returnvalue == 0:
         self.delState( PasswordList.STATE_MOUNTED )
      self._postProc( process )
      self.logEnd()
   
   def _loadFromFile( self ):
      self.logStart( "_loadFromFile" )
      with open( self.filename, "rb" ) as file:
         self._map = pickle.load( file )
      self.logEnd()
   
   def _saveToFile( self ):
      self.logStart( "_saveToFile" )
      with open( self.filename, "wb" ) as file:
         pickle.dump( self._map, file, pickle.HIGHEST_PROTOCOL )
      self.logEnd()
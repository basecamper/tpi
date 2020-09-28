import threading
from typing import Callable
from subprocess import Popen, PIPE, TimeoutExpired
from datetime import datetime

from lib.glob import SYSTEM_OK
from lib.log import Log

class ProcHandlerChain( Log ):
   
   def __init__( self,
                 procHandlerChain : list ):
      Log.__init__( self, "ProcHandlerChain" )
      self._procHandlerChain = procHandlerChain
      self._currentHandlerIndex = 0
      
      self._tempOnError = None
      self._tempOnSuccess = None
      self._hasProcessedOk = False
   
   def hasProcessedOk( self ):
      return 
   
   def addSuccessCallback( self, func : object ):
      self._parentOnSuccess.append( func )
      
   def addErrorCallback( self, func : object ):
      self._parentOnError.append( func )
   
   def run( self, onSuccess : object = None, onError : object = None ):
      self.logStart()
      self._currentHandlerIndex = 0
      self._tempOnError = onError
      self._tempOnSuccess = onSuccess
      self._runCurrentHandler()
      self.logEnd()
   
   def _getCurrentHandler( self ):
      self.log( "idx {i}".format( i=self._currentHandlerIndex ) )
      return self._procHandlerChain[ self._currentHandlerIndex ]
   
   def _runCurrentHandler( self ):
      self.logStart()
      self._getCurrentHandler().run( onSuccess=self.onSuccess, onError=self.onError )
      self.logEnd()
   
   def onSuccess( self ):
      self.logStart()
      handlerLen = len( self._procHandlerChain )
      self._currentHandlerIndex += 1
      self.log( "idx {i}/{m} successful".format( i=self._currentHandlerIndex , m=handlerLen ) )
      if self._currentHandlerIndex >= handlerLen:
         self.log( "chain successful {s}".format( s=bool(self._tempOnSuccess) ) )
         if self._tempOnSuccess:
            self.log( "running success callback func" )
            self._tempOnSuccess()
         self._hasProcessedOk = True
      else:
         self._runCurrentHandler()
      self.logEnd()
   
   def onError( self ):
      self.logStart()
      if self._tempOnError:
         self.log( "running error callback func" )
         self._tempOnError()
      self._hasProcessedOk = False
      self.logEnd()

class ProcHandler( Log ):
   
   def __init__( self,
                 command : list,
                 callback = None,
                 fullCallback = None,
                 onError = None,
                 onSuccess = None,
                 cooldown = 0,
                 timeout = 3,
                 stdin : str = None ):
      Log.__init__( self, "ProcHandler", "command: {command} cooldown: {c} timeout: {t}".format(command=command, c=cooldown, t=timeout) )
      
      self._command = command
      self._callback = [ callback ] if callback else []
      self._fullCallback = [ fullCallback ] if fullCallback else []
      self._onError = [ onError ] if onError else []
      self._onSuccess = [ onSuccess ] if onSuccess else []
      self._tempOnError = None
      self._tempOnSuccess = None
      self._cooldown = cooldown
      self._timeout = timeout
      self._cooldownTimestamp = None
      self._proc = None
      self._thread = None
      self._returnValue = None
      self._stdin = stdin.encode() if stdin else None
   
   def run( self, onError : object = None, onSuccess : object = None ):
      self.logStart( "has param: onSuccess {s} onError {e}".format( e=bool(onError), s=bool(onSuccess)) )
      
      
      if self._cooldown > 0:
         if self._evalSetTimestamp():
            self._tempOnError = onError
            self._tempOnSuccess = onSuccess
            self._runThread()
      else:
         self._runThread()
         self._tempOnError = onError
         self._tempOnSuccess = onSuccess
      
      self.logEnd()
   
   def addCallback( self, func : object ):
      self._callback.append( func )
   
   def addFullCallback( self, func : object ):
      self._fullCallback.append( func )
   
   def addSuccessCallback( self, func : object ):
      self._onSuccess.append( func )
      
   def addErrorCallback( self, func : object ):
      self._onError.append( func )
   
   def isProcessing( self ):
      return bool( self._thread and self._thread.isAlive() )
   
   def hasProcessedOk( self ):
      self.log( "{r}".format(
         r=bool( self._returnValue != None and self._returnValue == SYSTEM_OK ) ) )
      return bool( self._returnValue != None and self._returnValue == SYSTEM_OK )
   
   def _onProcessFinished( self, stdout, stderr ):
      self.logStart( "has functions: tempOnSuccess: {s}, tempOnError: {e}".format(
         e=bool(self._tempOnError), s=bool(self._tempOnSuccess) ) )
      
      if self.hasProcessedOk():
         if self._tempOnSuccess:
            self.log( "running self._tempOnSuccess()" )
            self._tempOnSuccess()
         for f in self._onSuccess:
            f()
      else:
         if self._tempOnError:
            self.log( "running self._tempOnError()" )
            self._tempOnError()
         for f in self._onError:
            f()
      
      self._tempOnError = None
      self._tempOnSuccess = None
      
      for f in self._fullCallback:
         f( self._proc )
      
      for f in self._callback:
         f( stdout, stderr )
      self.logEnd()
   def _getTimestampPassedSeconds( self, now : object = None ):
      return ( ( now or datetime.now() ) - self._cooldownTimestamp ).seconds
   
   def _evalSetTimestamp( self ):
      self.logStart()
      
      now = datetime.now()
      if not self._cooldownTimestamp or ( self._getTimestampPassedSeconds( now=now ) > self._cooldown ):
         self.logEnd( "cooldown passed, timestamp: {t} now: {n}".format( t=self._cooldownTimestamp, n=now ) )
         self._cooldownTimestamp = now
         return True
      return False
            
   def _runThread( self ):
      self.logStart()
      if not self.isProcessing():
         self.log( "not processing .. creating thread" )
         self._thread = threading.Thread(target=self._runInThread, args=( self._onProcessFinished, self._command ))
         self._thread = self._thread.start()
      self.logEnd()
   
   def _runInThread( self, func, args ):
      self.logStart( "args {a} input {i}".format( a=args, i=self._stdin ) )
      stdout, stderr = None, None
      
      if self._stdin != None:
         self.log( "creating subprocess with stdin pipe" )
         self._proc = Popen( args, stdout=PIPE, stdin=PIPE, close_fds=True )
      else:
         self.log( "creating subprocess" )
         self._proc = Popen( args, stdout=PIPE, close_fds=True )
      
      if self._timeout > 0:
         try:
            self.log( "communicating..." )
            if self._stdin != None:
               stdout, stderr = self._proc.communicate( timeout=self._timeout, input=self._stdin )
            else:
               stdout, stderr = self._proc.communicate( timeout=self._timeout )
               
            self.log( "subprocess finished, command: {c}".format( c=args ) )
         except TimeoutExpired:
            self._proc.kill()
            self.log( "subprocess cancelled due to timeout, command: {c}".format( c=args ) )
      else:
         if self._stdin != None:
            stdout, stderr = self._proc.communicate( input=self._stdin )
         else:
            stdout, stderr = self._proc.communicate()
      
      self._returnValue = self._proc.returncode
      
      if func:
         self.log( "running callback func" )
         func( stdout, stderr )
      
      self.logEnd( "stdout: {o} stderr: {e}".format( o=bool( stdout ), e=bool( stderr ) ) )
      
      return ( stdout, stderr )
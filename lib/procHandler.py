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
      self.logEvent( "run" )
      self._currentHandlerIndex = 0
      self._tempOnError = onError
      self._tempOnSuccess = onSuccess
      self._runCurrentHandler()
   
   def _getCurrentHandler( self ):
      self.logEvent( "gettingCurrentHandler at idx {i}".format( i=self._currentHandlerIndex ) )
      return self._procHandlerChain[ self._currentHandlerIndex ]
   
   def _runCurrentHandler( self ):
      self._getCurrentHandler().run( onSuccess=self.onSuccess, onError=self.onError )
   
   def onSuccess( self ):
      handlerLen = len( self._procHandlerChain )
      self._currentHandlerIndex += 1
      self.logEvent( "onSuccess idx {i}/{m}".format( i=self._currentHandlerIndex , m=handlerLen ) )
      if self._currentHandlerIndex >= handlerLen:
         self.logEvent( "onSuccess","self._tempOnSuccess {s}".format( s=bool(self._tempOnSuccess) ) )
         if self._tempOnSuccess:
            self._tempOnSuccess()
         self._hasProcessedOk = True
      else:
         self._runCurrentHandler()
   
   def onError( self ):
      self.logEvent( "onError","self._tempOnError {s}".format( s=bool(self._tempOnSuccess) ) )
      if self._tempOnError:
         self._tempOnError()
      self._hasProcessedOk = False

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
      Log.__init__( self,
                    className="ProcHandler",
                    message="command {command} cooldown {c} timeout {t}".format(command=command, c=cooldown, t=timeout) )
      
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
      self.logStart( "run","onSuccess {s} onError {e}".format( e=bool(onError), s=bool(onSuccess)) )
      
      
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
      self.logEvent( "hasProcessedOk","{r}".format( r=bool( self._returnValue != None and self._returnValue == SYSTEM_OK ) ) )
      return bool( self._returnValue != None and self._returnValue == SYSTEM_OK )
   
   def _onProcessFinished( self, stdout, stderr ):
      self.logEvent( "_onProcessFinished","temp onSuccess {s} onError {e}".format( e=bool(self._tempOnError), s=bool(self._tempOnSuccess) ) )
      
      if self.hasProcessedOk():
         if self._tempOnSuccess:
            self.logEvent( "_onProcessFinished","self._tempOnSuccess()" )
            self._tempOnSuccess()
         for f in self._onSuccess:
            f()
      else:
         if self._tempOnError:
            self.logEvent( "_onProcessFinished","self._tempOnError()" )
            self._tempOnError()
         for f in self._onError:
            f()
      
      self._tempOnError = None
      self._tempOnSuccess = None
      
      for f in self._fullCallback:
         f( self._proc )
      
      for f in self._callback:
         f( stdout, stderr )
   
   def _getTimestampPassedSeconds( self, now : object = None ):
      return ( ( now or datetime.now() ) - self._cooldownTimestamp ).seconds
   
   def _evalSetTimestamp( self ):
      self.logStart( "_evalSetTimestamp" )
      
      now = datetime.now()
      if not self._cooldownTimestamp or ( self._getTimestampPassedSeconds( now=now ) > self._cooldown ):
         self.logEnd( "cooldown passed, timestamp: {t} now: {n}".format( t=self._cooldownTimestamp, n=now ) )
         self._cooldownTimestamp = now
         return True
      
      self.logEnd( printMessage=False )
      return False
            
   def _runThread( self ):
      self.logStart( "_runThread" )
      if not self.isProcessing():
         self.log( "not processing .. creating thread" )
         self._thread = threading.Thread(target=self._runInThread, args=( self._onProcessFinished, self._command ))
         self._thread = self._thread.start()
      self.logEnd()
   
   def _runInThread( self, func, args ):
      self.logEvent( method="_runInThread", message="starting, args {a} input {i}".format( a=args, i=self._stdin ) )
      if self._stdin != None:
         self._proc = Popen( args, stdout=PIPE, stdin=PIPE, close_fds=True )
      else:
         self._proc = Popen( args, stdout=PIPE, close_fds=True )
      
      if self._timeout > 0:
         try:
            if self._stdin != None:
               stdout, stderr = self._proc.communicate( timeout=self._timeout, input=self._stdin )
            else:
               stdout, stderr = self._proc.communicate( timeout=self._timeout )
               
            self.logEvent( method="_runInThread", message="subprocess finished command: {c}".format( c=args ) )
         except TimeoutExpired:
            self._proc.kill()
            self.logEvent( method="_runInThread", message="subprocess due to timeout cancelled! command: {c}".format( c=args ) )
      else:
         if self._stdin != None:
            stdout, stderr = self._proc.communicate( input=self._stdin )
         else:
            stdout, stderr = self._proc.communicate() # TODO cmon ... 4 calls
      self._returnValue = self._proc.returncode
      if func:
         func( stdout, stderr )
      return ( stdout, stderr )
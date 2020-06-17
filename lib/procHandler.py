import threading
from typing import Callable
from subprocess import Popen, PIPE
from datetime import datetime

from lib.log import Log

class ProcHandler( Log ):
   
   def __init__( self,
                 command : list,
                 callback = None,
                 fullCallback = None,
                 cooldown = 0,
                 timeout = 3 ):
      Log.__init__( self,
                    className="ProcHandler",
                    message="command {command} cooldown {c} timeout {t}".format(command=command, c=cooldown, t=timeout) )
      
      self._command = command
      self._callback = callback
      self._fullCallback = fullCallback
      self._cooldown = cooldown
      self._timeout = timeout
      self._cooldownTimestamp = None
      self._proc = None
      self._thread = None
   
   def run( self ):
      self.logStart( "run" )
      
      if self._cooldown > 0:
         if self._evalSetTimestamp():
            self._runThread()
      else:
         self._runThread()
      
      self.logEnd()
   
   def _onProcessFinished( self, stdout, stderr ):
      if self._fullCallback != None:
         self._fullCallback( self._proc )
      
      if self._callback != None:
         self._callback( stdout, stderr )
   
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
      if not self._thread or not self._thread.isAlive():
         self.log( "creating thread {c}".format( c=self._command ) )
         self._thread = threading.Thread(target=self._runInThread, args=( self._onProcessFinished, self._command ))
         self._thread = self._thread.start()
      self.logEnd()
   
   def _runInThread( self, func, args ):
      self._proc = Popen( args, stdout=PIPE, close_fds=True )
      if self._timeout > 0:
         try:
            stdout, stderr = self._proc.communicate(timeout=self._timeout)
            self.logEvent( method="_runInThread", message="subprocess finished command: {c}".format( c=args ) )
         except TimeoutExpired:
            self.proc.kill()
            self.logEvent( method="_runInThread", message="subprocess due to timeout cancelled! command: {c}".format( c=args ) )
      else:
         stdout, stderr = self._proc.communicate()
      if func:
         func( stdout, stderr )
      return ( stdout, stderr )
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
                 interval = 0,
                 timeout = 3 ):
      Log.__init__( self,
                    className="ProcHandler",
                    message="command {command} interval {i} timeout {t}".format(command=command, i=interval, t=timeout) )
      
      self.command = command
      self.callback = callback
      self.fullCallback = fullCallback
      self.interval = interval
      self.timeout = timeout
      self.intervalTimestamp = None
      self.proc = None
      self.thread = None
   
   def _callback( self, stdout, stderr ):
      if self.fullCallback != None:
         self.fullCallback( self.proc )
      
      if self.callback != None:
         self.callback( stdout, stderr )
   
   def run( self ):
      self.logStart( "run" )
      if self.interval > 0:
         if self._evalSetTimestamp():
            self.log("interval reached")
            self._runThread()
      else:
         self._runThread()
      self.logEnd()

   def _evalSetTimestamp( self ):
      if (    self.intervalTimestamp == None
           or ( datetime.now() - self.intervalTimestamp ).seconds > self.interval ):
         self.intervalTimestamp = datetime.now()
         return True
      return False
            
   def _runThread( self ):
      self.logStart( "_runThread" )
      if not self.thread or not self.thread.isAlive():
         self.log( "creating thread {c}".format( c=self.command ) )
         self.thread = threading.Thread(target=self._runInThread, args=( self._callback, self.command ))
         self.thread = self.thread.start()
      self.logEnd()
   
   def _runInThread( self, func, args ):
      self.proc = Popen( args, stdout=PIPE, close_fds=True )
      if self.timeout > 0:
         try:
            stdout, stderr = self.proc.communicate(timeout=self.timeout)
            self.logEvent( method="_runInThread", message="subprocess finished command: {c}".format( c=args ) )
         except TimeoutExpired:
            self.proc.kill()
            self.logEvent( method="_runInThread", message="subprocess due to timeout cancelled! command: {c}".format( c=args ) )
      else:
         stdout, stderr = self.proc.communicate()
      if func:
         func( stdout, stderr )
      return ( stdout, stderr )
from typing import Callable
import threading
from subprocess import Popen, PIPE
from datetime import datetime
from lib.log import Log

class ProcHandler:
   
   def __init__( self,
                 command : list,
                 callback,
                 interval = 0,
                 timeout = 3 ):
      Log.debug("INIT ProcHandler command {command} interval {i} timeout {t}".format(command=command, i=interval, t=timeout))
      self.command = command
      self.callback = callback
      self.interval = interval
      self.timeout = timeout
      self.intervalTimestamp = None
      self.proc = None
      self.thread = None
   
   def run( self ):
      Log.debug("ProcHandler.run()")
      if self.interval > 0:
         if self._eval_set_timestamp():
            self._run_thread()
      else:
         self._run_thread()

   def _eval_set_timestamp( self ):
      if (    self.intervalTimestamp == None
           or ( datetime.now() - self.intervalTimestamp ).seconds > self.interval ):
         self.intervalTimestamp = datetime.now()
         return True
      return False
            
   def _run_thread(self):
      if not self.thread or not self.thread.isAlive():
         Log.debug("ProcHandler._run_thread()")
         self.thread = threading.Thread(target=self._run_in_thread, args=( self.callback, self.command ))
         self.thread = self.thread.start()  
   
   def _run_in_thread( self, func, args ):
      self.proc = Popen( args, stdout=PIPE, close_fds=True )
      if self.timeout > 0:
         try:
            stdout, stderr = self.proc.communicate(timeout=self.timeout)
         except TimeoutExpired:
            self.proc.kill()
      else:
         stdout, stderr = self.proc.communicate()
      func( stdout, stderr )
      return ( stdout, stderr )
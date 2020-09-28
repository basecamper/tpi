import sys
import inspect

from lib.glob import Global
from lib.tools import EMPTY_STRING, getMsTimestamp

class Log( object ):
   _statusLines = []
   _popStatusTimestamp = None
   _wasStatusChecked = True
   def __init__( self, className : str ):
      self._className = className
   
   def logStart( self, message : str = None ):
      Log2.debug( Log2._formatMessage(
         prefix="START ",
         className=self._className,
         method=inspect.stack()[1].function,
         message=message
      ) )
   
   def log( self, message : str = None ):
      Log2.debug( Log2._formatMessage(
         prefix="      ",
         className=self._className,
         method=inspect.stack()[1].function,
         message=message
      ) )
   def logEnd( self, message : str = None ):
      Log2.debug( Log2._formatMessage(
         prefix="END   ",
         className=self._className,
         method=inspect.stack()[1].function,
         message=message
      ) )
   
   def logError( self, message : str = None, method : str = None ):
      stack = inspect.stack()
      for f in stack:
         Log2.debug( Log2._formatMessage(
            prefix="ERROR ",
            className=self._className,
            method=method if method else inspect.stack()[1].function,
            message="{n}: {m}".format(
               n=stack.index( f ),
               m=f.function )
         ) )
      
      Log2.debug( Log2._formatMessage(
         prefix="ERROR ",
         className=self._className,
         method=inspect.stack()[1].function,
         message=message
      ) )
   
   def logException( self, e : Exception ):
      self.logError( message="Exception: {e}".format( e=e ),
                     method=inspect.stack()[1].function )
   
   @staticmethod
   def debug( message : str ):
      if message:
         if Global.DEBUG_PRINT or Global.DEBUG:
            sys.stderr.write( "{m} \n".format( m=message ) )
   
   @staticmethod
   def _formatMessage( prefix : str, className : str, method : str, message : str = None ):
      Log2.debug( [ prefix, className, method, message ] )
      return "{p}{c}{me}{m}".format( p=prefix,
                                    c=className,
                                    me=method,
                                    m=" {im}".format( im=message ) if message else EMPTY_STRING ) 
   
   @staticmethod
   def pushStatus( message, color ):
      Log._statusLines.append( ( message, color ) )
      Log._wasStatusChecked = False

import sys
import inspect

from lib.glob import Global
from lib.tools import EMPTY_STRING, getMsTimestamp

class Log( object ):
   _statusLines = []
   _popStatusTimestamp = None
   _wasStatusChecked = True
   
   def __init__( self, className : str = None, message : str = None, printMessage : bool = True ):
      object.__init__( self )
      self._methodNames = []
      self._className = className
      if printMessage:
         Log.debug( message="INIT  {m}".format( m=self.formatMsg( "__init__", message ) ) )
         
   
   def getClassName( self ):
      return self._className
   
   @staticmethod
   def _formatMsg( className : str, method : str, message : str ):
      return "{c}{s}{m}{s2}{t}".format( c=className,
                                        s="." if className and method else EMPTY_STRING,
                                        m=method or EMPTY_STRING,
                                        s2=" " if message else EMPTY_STRING,
                                        t=message if message else EMPTY_STRING ) 
   
   def formatMsg( self, method : str, message : str = None ):
      return Log._formatMsg( className=self.getClassName(), method=method, message=message )
   
   def logStart( self, method : str, message : str = None, printMessage : bool = True ):
      self._methodNames.append( method )
      if printMessage:
         Log.debug( message="START {m}".format( m=self.formatMsg( method, message ) ) )
   
   def log( self, message : str, logMethod : bool = True ):
      method = None
      if logMethod and len(self._methodNames) > 0:
         method = self._methodNames[-1]
      Log.debug( message="      {m}".format( m=self.formatMsg( method, message ) ) )
   
   def logError( self, message : str, logMethod : bool = True ): # TODO printMessage and logMethod
      method = None
      if logMethod and len(self._methodNames) > 0:
         method = self._methodNames[-1]
      Log.debug( message="ERROR {m}".format( m=self.formatMsg( method, message ) ) )
   
   def logEvent( self, method : str = None, message : str = None ):
      Log.debug( message="EVENT {m}".format( m=self.formatMsg( method=method, message=message ) ) )
   
   def logEnd( self, message : str = None, printMessage : bool = True ):
      method = self._methodNames.pop()
      if printMessage:
         Log.debug( message="END   {m}".format( m=self.formatMsg( method, message ) ) )
   
   def logException( self, exception : Exception, message : str = "" ):
      Log.debug( message="ERROR {emsg}".format( emsg=self.formatMsg( message="{m} EXCEPTION: {e}".format( m=message, e=exception ) ) ) )
   
   @staticmethod
   def wasStatusChecked():
      return bool( Log._wasStatusChecked )
   
   @staticmethod
   def debug( className : str = None, method : str = None, message : str = None ):
      if message:
         if Global.DEBUG_PRINT or Global.DEBUG:
            sys.stderr.write( "{m} \n".format( m=message ) )
   
   @staticmethod
   def pushStatus( message, color ):
      Log._statusLines.append( ( message, color ) )
      Log._wasStatusChecked = False
   
   @staticmethod
   def popStatus():
      Log._wasStatusChecked = True
      if len( Log._statusLines ):
         now = getMsTimestamp()
         if (    not Log._popStatusTimestamp
              or Log._popStatusTimestamp < now - 100 ):
            Log._popStatusTimestamp = now
            return Log._statusLines.pop(0)
      return ( None, None )
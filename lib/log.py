import sys
import inspect

from lib.glob import Global
from lib.tools import EMPTY_STRING, getMsTimestamp

class Log( object ):
   _statusLines = []
   _popStatusTimestamp = None
   _wasStatusChecked = True
   def __init__( self, className : str, initMessage : str = None ):
      self._className = className
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log.debug(
            Log._formatMessage(
               prefix="INIT  ",
               className=self._className,
               method=stack[1].function,
               message=initMessage,
               stack=stack ) )
   
   def getClassName( self ):
      return self._className
   
   def logStart( self, message : str = None ):
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log.debug(
            Log._formatMessage(
               prefix="START ",
               className=self._className,
               method=stack[1].function,
               message=message,
               stack=stack ) )
   
   def log( self, message : str = None ):
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log.debug(
            Log._formatMessage(
               prefix="      ",
               className=self._className,
               method=stack[1].function,
               message=message,
               stack=stack ) )
   
   def logEnd( self, message : str = None ):
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log.debug(
            Log._formatMessage(
               prefix="END   ",
               className=self._className,
               method=stack[1].function,
               message=message,
               stack=stack ) )
   
   def logError( self, message : str = None ):
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log._logStack( stack,
                        self._className,
                        stack[1].function )
         
         Log.debug(
            Log._formatMessage(
               prefix="ERROR ",
               className=self._className,
               method=stack[1].function,
               message=message,
               stack=stack ) )
   
   def logException( self, e : Exception ):
      if Global.DEBUG_PRINT or Global.DEBUG:
         stack = inspect.stack()
         Log._logStack( stack, self._className, stack[1].function )
         
         Log.debug(
            Log._formatMessage(
               prefix="ERROR ",
               className=self._className,
               method=stack[1].function,
               message="EXCEPTION: {e}".format( e=e ),
               stack=stack
               ) )
   
   @staticmethod
   def _logStack( stack, className : str, method : str ):
      for f in stack:
         Log.debug( Log._formatMessage(
               prefix="STACK ",
               className=className,
               method=method,
               message="{n}: {m}".format(
                  n=stack.index( f ),
                  m=f.function ),
               stack=stack ) )
   
   @staticmethod
   def _formatMessage( prefix : str, className : str, method : str, message : str = None, stack = None ):
      
      indent = ""
      iAmount = (      len( stack ) - Global.LOG_REDUCE_INDENT
                  if   Global.LOG_REDUCE_INDENT < len( stack )
                  else 0 )
      if iAmount > 0:
         indent = " " * iAmount
      
      return "{p}{i}{c} {me}{m}".format( i=indent,
                                         p=prefix,
                                         c=className,
                                         me=method,
                                         m=" {im}".format( im=message ) if message else EMPTY_STRING ) 
   
   @staticmethod
   def debug( message : str ):
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
   
   @staticmethod
   def wasStatusChecked():
      return bool( Log._wasStatusChecked )

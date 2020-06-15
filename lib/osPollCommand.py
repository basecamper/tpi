from lib.screen.screenColor import Color
from lib.log import Log
import re as re

def getColorInRange( value : float, firstRangeTop : float, secondRangeTop : float ):
   if value < firstRangeTop:
      return Color.GREEN
   elif value < secondRangeTop:
      return Color.YELLOW
   else:
      return Color.RED

def matchColorFunction( text : str, valueColorMap : dict = {} ):
   for k, v in valueColorMap.items():
      if k == text:
         return v

class OSPollCommand:
   @staticmethod
   def getCommand():
      return [ "echo", "-" ]
   
   @staticmethod
   def getCommand( obj ):
      return obj.getCommand()
   
   @staticmethod
   def parseFunction( stdout, stderr ):
      return '-', Color.DEFAULT

class GetGPUTempCommand( OSPollCommand ):
   @staticmethod
   def getCommand():
      return ['/opt/vc/bin/vcgencmd', 'measure_temp']
   @staticmethod
   def parseFunction( stdout, stderr ):
      t = stdout.decode('utf-8')
      t = "%s.%s" % ( t[5:7], t[8] )
      Log.debug("GetGPUTempCommand","parsed {text}".format(text=t))
      return "{t}°C".format( t=t ), getColorInRange( float( t ), 55, 65 )

class GetCPUTempCommand(OSPollCommand):
   @staticmethod
   def getCommand():
      return ['cat','/sys/class/thermal/thermal_zone0/temp']
   @staticmethod
   def parseFunction( stdout, stderr ):
      t = stdout.decode('utf-8')
      t = "%s.%s" % ( t[0:2], t[2] )
      Log.debug("GetCPUTempCommand","parsed {text}".format(text=t))
      return "{t}°C".format( t=t ), getColorInRange( float( t ), 55, 65 )

class GetGPUMemUsageCommand(OSPollCommand):
   @staticmethod
   def getCommand():
      return ['vcdbg','reloc']
   @staticmethod
   def parseFunction( stdout, stderr ):
      t = stdout.decode('utf-8')
      free = re.search( r"([0-9])*M free memory", t, re.M ).group(0)
      free = re.search( r"([0-9])*", free, re.M ).group(0)
      alloc = re.search( r"allocated is [0-9]*M", t ).group(0).split(" ")[2].replace("M","")
      
      f = int( free )
      a = int( alloc )
      p = a / ( f + a ) * 100
      
      return "{percent}%".format( percent=int( p ) ), getColorInRange( float( p ), 70, 85 )

   
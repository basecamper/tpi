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

class OSCommand:
   @staticmethod
   def getStatusCommand(): return None
   @staticmethod
   def getStartCommand(): return None
   @staticmethod
   def getStopCommand(): return None
   @staticmethod
   def parseStatus( stdout, stderr ): return None, None
   @staticmethod
   def parseStatus( stdout, stderr ): return None, None
   @staticmethod
   def parseStart( stdout, stderr ): return None, None
   @staticmethod
   def parseStop( stdout, stderr ): return None, None

class PoweroffCommand(OSCommand):
   @staticmethod
   def getStartCommand():
      return ['poweroff']



class DisplaySplashImageCommand(OSCommand):
   @staticmethod
   def getStartCommand():
      return ['dd','if=/opt/splash.bmp','of=/dev/fb1','bs=655555','count=1','status=none']

class WpaSupplicantCommand(OSCommand):
   @staticmethod
   def getStartCommand():
      return ['systemctl','start','wpa_supplicant']
   @staticmethod
   def getStopCommand():
      return ['systemctl','stop','wpa_supplicant']

class EnableWlanInterfaceCommand(OSCommand):
   @staticmethod
   def getStartCommand():
      return ['ifconfig','wlan0','up']
   @staticmethod
   def getStopCommand():
      return ['ifconfig','wlan0','down']

class EnableWlanWifiCommand(OSCommand):
   @staticmethod
   def getStartCommand():
      return ['iwconfig','wlan0','power','on']
   @staticmethod
   def getStopCommand():
      return ['iwconfig','wlan0','power','off']

import json

from lib.glob import Global

class ConfigReader:
   
   instance = None
   
   @staticmethod
   def getInstance():
      if not ConfigReader.instance:
         ConfigReader.instance = ConfigReader( Global.CONFIG_FILE )
      return ConfigReader.instance
   
   def __init__( self, filePath : str ):
      self._data = None
      with open( filePath ) as f:
         self._data = json.load( f )
   
   def getData( self ):
      return self._data

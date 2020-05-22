class OSComplexCommand():
   @staticmethod
   def getStatusCommand(): pass
   @staticmethod
   def getStartCommand(): pass
   @staticmethod
   def getStopCommand(): pass
   @staticmethod
   def parseStatus( stdout, stderr ): pass
   @staticmethod
   def parseStatus( stdout, stderr ): pass
   @staticmethod
   def parseStart( stdout, stderr ): pass
   @staticmethod
   def parseStop( stdout, stderr ): pass


class GetIwconfigCommand(OSComplexCommand):
   @staticmethod
   def getCommand():
      return ["iwconfig"]
   
   @staticmethod
   def getCommand( interface : str ):
      return ["iwconfig", interface]
   
   @staticmethod
   def parseInterfaces( stdout, stderr, interfaces = None ): pass

class GetIfconfigCommand(OSComplexCommand):
   @staticmethod
   def getCommand():
      return ["ifconfig"]
   
   @staticmethod
   def getCommand( interface : str ):
      return ["ifconfig", interface]
   
   @staticmethod
   def parseFunction( stdout, stderr ):
      return ""
   
   @staticmethod
   def _parseObject( text : str ):
      obj.isUp =      bool( re.search( r"^.*:.*<.*UP.*>.*$", text, re.MULTILINE ) != None )
      obj.ipAddr =    re.search( r"inet [0-9.]*", text, re.MULTILINE ).group(0)[5:]
      obj.ip6Addr =   re.search( r"inet6 [0-9a-fA-F:]*", text, re.MULTILINE ).group(0)[6:]
      obj.netMask =   re.search( r"netmask [0-9.]*", text, re.MULTILINE ).group(0)[8:]
      obj.broadcast = re.search( r"broadcast [0-9.]*", text, re.MULTILINE ).group(0)[10:]
      obj.macAddr   = re.search( r"ether [0-9.]*", text, re.MULTILINE ).group(0)[6:]
   
   @staticmethod
   def parseInterfaces( stdout, stderr, interfaces = None ):
      text = stdout.decode('utf-8')
      _interfaces = interfaces or []
      for i in re.findall( r"^.*:.*$", t, re.MULTILINE ):
         interfaceName = re.search( r"^.*:", i ).group(0)[:-1]
         pat = re.compile( "{i}.*\n( .*\n)*".format( i=interfaceName ), re.MULTILINE )
         filteredText = pat.search( text ).group(0)
         interface = next( i for i in _interfaces if i.name == interfaceName )
         if not interface:
            interface = { "name" : interfaceName }
            _interfaces.append( interface )
         GetIfconfigCommand._parseObject( filteredText, interface )
      return _interfaces


#class EnableWifiCommand(OSComplexCommand):
#   @staticmethod
#   def getStartCommand( interface ):
#      return ['ifconfig',interface,'up']
#   @staticmethod
#   def getStopCommand():
#      return ['ifconfig',interface,'down']
from enum import Enum
from lib.screen.screenColor import Color
from lib.log import Log

class InteractiveElement:
   def __init__( self, children : list ):
      self._children = children
   
   def addChild( self, child ):
      self._children.append( child )
   
   def addChildren( self, children ):
      for c in children:
         self._children.append( c )
   
   def emptyChildren( self ):
      self._children = []
   
   def getChildren( self ):
      return self._children
   
   def run( self ):
      Log.debug("InteractiveElement.run() children len {len}".format( len=len(self._children) ))
      for child in self.getChildren():
         child.run()
      Log.debug( "InteractiveElement.run() OK" )
      return ScreenReturn.OK
   
   def onButtonDown( self, button ):
      for c in self._children:
         returnValue = c.onButtonDown( button )
         if returnValue != ScreenReturn.OK:
            return returnValue
      return ScreenReturn.OK


class ScreenElement( InteractiveElement ):
   def __init__( self,
                 text = None,
                 color = Color.DEFAULT,
                 isEndingLine = None,
                 children = None,
                 index = -1 ):
      Log.debug(
         "INIT ScreenElement, text: {text} color: {color} isEndingLine {isEndingLine} children {children} index {idx}".format(
            text=text,
            color=color,
            isEndingLine=isEndingLine,
            children=bool(children),
            idx=index ) )
      
      super().__init__( children or [] )
      self.text = text
      self.color = color
      self.isEndingLine = isEndingLine or False
      self.index = index

class ScreenReturn(Enum):
   ERROR = 0,
   OK = 1,
   YES = 2,
   NO = 3,
   NEXT = 4,
   PREV = 5
from enum import Enum

from lib.log import Log
from lib.screen.screenColor import Color

class InteractiveElement( Log ):
   def __init__( self,
                 children : list = None,
                 buttonProcMap : dict = None ):
      Log.__init__( self, "InteractiveElement", printMessage=False )
      self._children = children or []
      self._exclusivePropagation = False
      self._enablePropagation = True
      self.buttonProcMap = {} if buttonProcMap == None else buttonProcMap
   
   def setExclusivePropagation( self, state : bool ):
      self._exclusivePropagation = state
   
   def isExclusivePropagationRequired( self ):
      return bool( self._exclusivePropagation )
   
   def setEnablePropagation( self, state : bool ):
      self._enablePropagation = state
   
   def isPropagationEnabled( self ):
      return bool( self._enablePropagation )
   
   def addChild( self, child ):
      self._children.append( child )
   
   def addChildren( self, children : list ):
      for c in children:
         self._children.append( c )
   
   def emptyChildren( self ):
      self._children = []
   
   def getChildren( self ):
      return self._children
   
   def run( self ):
      for child in self.getChildren():
         child.run()
   
   # return True if a child required an exclusive callback
   def propagateExclusiveButtonDown( self, button ):
      self.logStart( "propagateExclusiveButtonDown", printMessage=False )
      propagated = False
      
      if self.isExclusivePropagationRequired():
         buttonProc = self.buttonProcMap.get( button )
         if buttonProc:
            self.log( message="button {b}".format( b=button ) )
            self.onButtonDown( button )
            propagated = True
         else:
            self.log( message="button {b} not in buttonProcMap".format( b=button ) )
      
      for c in self.getChildren():
         propagated |= c.propagateExclusiveButtonDown( button )
      
      self.logEnd( printMessage=False )
      return propagated
   
   def onButtonDown( self, button ):
      self.logStart( "onButtonDown", printMessage=False )
      buttonProc = self.buttonProcMap.get( button )
      if buttonProc != None:
         buttonProc( button )
      
      if self.isPropagationEnabled():
         for c in self._children:
            returnValue = c.onButtonDown( button )
      else:
         self.log( message="propagation blocked button: {b}".format( b=button ) )
      self.logEnd( printMessage=False )


class ScreenElement( InteractiveElement, Log ):
   def __init__( self,
                 text = None,
                 color = Color.DEFAULT,
                 isEndingLine = None,
                 children = None,
                 index = -1,
                 buttonProcMap : dict = None ):
      
      InteractiveElement.__init__( self,
                                   children=children,
                                   buttonProcMap=buttonProcMap )
      Log.__init__(  self,
                     "ScreenElement",
                     "text: {t} color: {col} isEndingLine {l} children {ch} index {i}".format(  t=text,
                                                                                                col=color,
                                                                                                l=isEndingLine,
                                                                                                ch=bool(children),
                                                                                                i=index ) )
      self.text = text
      self.color = color
      self.isEndingLine = isEndingLine or False
      self.index = index
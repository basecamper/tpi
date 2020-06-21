from enum import Enum

from lib.log import Log
from lib.screen.screenColor import Color

class InteractiveElement( Log ):
   def __init__( self,
                 children : list = None,
                 buttonDownMap : dict = None ):
      Log.__init__( self, "InteractiveElement", printMessage=False )
      self._children = children or []
      self._exclusivePropagation = False
      self._enablePropagation = True
      self._enableButtonDownMap = True
      self.buttonDownMap = {} if buttonDownMap == None else buttonDownMap
   
   def setExclusivePropagation( self, state : bool ):
      self.logStart( "setExclusivePropagation","state: {s}".format( s=state ))
      self._exclusivePropagation = state
      self.logEnd( printMessage=False )
   
   def hasExclusivePropagation( self ):
      return bool( self._exclusivePropagation )
   
   def setEnablePropagation( self, state : bool ):
      self.logStart( "setEnablePropagation","state: {s}".format( s=state ))
      self._enablePropagation = state
      self.logEnd( printMessage=False )
   
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
   
   def isButtonDownMapEnabled( self ):
      return bool( self._enableButtonDownMap )
   
   def setButtonDownMapActive( self, state : bool ):
      self.logStart( "setButtonDownMapActive","state: {s}".format( s=state ))
      self._enableButtonDownMap = state
      self.logEnd( printMessage=False )
   
   # return True if a child required an exclusive callback
   def propagateExclusiveButtonDown( self, button ):
      self.logStart( "propagateExclusiveButtonDown", printMessage=False )
      propagated = False
      
      if self.hasExclusivePropagation():
         buttonProc = self.buttonDownMap.get( button )
         if buttonProc:
            self.log( message="button {b}".format( b=button ) )
            self.onButtonDown( button )
            propagated = True
         else:
            self.log( message="button {b} not in buttonDownMap".format( b=button ) )
      
      if not self.hasExclusivePropagation() or self.isPropagationEnabled():
         for c in self.getChildren():
            propagated |= c.propagateExclusiveButtonDown( button )
      
      self.logEnd( printMessage=False )
      return propagated
   
   def onButtonDown( self, button ):
      self.logStart( "onButtonDown", printMessage=False )
      buttonProc = self.buttonDownMap.get( button )
      if buttonProc != None and self.isButtonDownMapEnabled():
         buttonProc( button )
      
      if self.isPropagationEnabled():
         for c in self._children:
            returnValue = c.onButtonDown( button )
      else:
         self.log( message="propagation blocked" )
      self.logEnd( printMessage=False )


class ScreenElement( InteractiveElement, Log ):
   def __init__( self,
                 text = None,
                 color = Color.DEFAULT,
                 isEndingLine = None,
                 children = None,
                 index = -1,
                 buttonDownMap : dict = None ):
      
      InteractiveElement.__init__( self,
                                   children=children,
                                   buttonDownMap=buttonDownMap )
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
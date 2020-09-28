from enum import Enum

from lib.log import Log
from lib.screen.screenColor import Color

class ScreenElement( Log ):
   def __init__( self,
                 text = None,
                 color = Color.DEFAULT,
                 isEndingLine = None,
                 children = None,
                 index = -1,
                 buttonDownMap : dict = None ):
      
      Log.__init__( self, "ScreenElement", "text: {t} color: {col} isEndingLine: {l} children: {ch}".format( 
            t=text,
            col=color,
            l=isEndingLine,
            ch=len( children ) if children else 0
         ) )
      self.text = text
      self.color = color
      self.isEndingLine = isEndingLine or False
      
      
      self._children = children or []
      self._exclusivePropagation = False
      self._enablePropagation = True
      self._enableButtonDownMap = True
      self.buttonDownMap = {} if buttonDownMap == None else buttonDownMap
   
   def setExclusivePropagation( self, state : bool ):
      self.logStart( "state: {s}".format( s=state ))
      self._exclusivePropagation = state
      self.logEnd()
   
   def hasExclusivePropagation( self ):
      return bool( self._exclusivePropagation )
   
   def setEnablePropagation( self, state : bool ):
      self.logStart( "state: {s}".format( s=state ))
      self._enablePropagation = state
      self.logEnd()
   
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
      self.logStart( "state: {s}".format( s=state ))
      self._enableButtonDownMap = state
   
   # return True if a child required an exclusive callback
   def propagateExclusiveButtonDown( self, button ):
      propagated = False
      
      if self.hasExclusivePropagation():
         propagated = True
         # even if button is not in map, count as propagated
         # to make sure normal propagation isn't executed afterwards
         buttonProc = self.buttonDownMap.get( button )
         if buttonProc:
            self.log( "button {b}".format( b=button ) )
            self.onButtonDown( button )
         else:
            self.log( "button {b} not in buttonDownMap".format( b=button ) )
      
      if not self.hasExclusivePropagation() or self.isPropagationEnabled():
         for c in self.getChildren():
            propagated |= c.propagateExclusiveButtonDown( button )
      
      return propagated
   
   def onButtonDown( self, button ):
      self.logStart()
      buttonProc = self.buttonDownMap.get( button )
      if buttonProc != None and self.isButtonDownMapEnabled():
         buttonProc( button )
      
      if self.isPropagationEnabled():
         for c in self._children:
            returnValue = c.onButtonDown( button )
      else:
         self.log( "propagation blocked" )
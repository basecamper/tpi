from lib.glob import Global, GlobalRuntime
from lib.log import Log
from lib.tools import getMsTimestamp
from lib.cursesWindow import CursesWindow
from lib.screen.overview import Overview
from lib.screen.screenColor import Color


class ScreenManager( Log ):
   
   def __init__( self ):
      Log.__init__( self, className="ScreenManager" )
      self.cursesWindow = CursesWindow() if not Global.DEBUG else None
      self.screen = Overview()
      self.isRefreshing = False
      self._lastRunTimestamp = None
      self._maxRunInterval = Global.MAIN_RUN_SECONDS
      self._setTimestamp()
   
   def __del__( self ):
      del( self.cursesWindow )
      del( self.screen )
      del( self )
   
   def onButtonDown( self, button ):
      if not self.screen.propagateExclusiveButtonDown( button ):
         self.screen.onButtonDown( button )
      self._run() # be very responsive and run regardless of lastRunTimestamp
      
   def _setTimestamp( self ):
      self._lastRunTimestamp = getMsTimestamp()
   
   # @return True if its time for a run
   def _evalTimestamp( self ):
      return self._lastRunTimestamp < getMsTimestamp() - ( self._maxRunInterval * 1000 )
   
   def run( self, evalReturn = True ):
      if self._evalTimestamp():
         self._run()
   
   def _run( self ):
      self._setTimestamp()
      self.logStart()
      if not self.isRefreshing and GlobalRuntime.refreshScreen:
         
         self.isRefreshing = True
         
         self.log( "Refreshing main screen..." )
         self.screen.run()
         
         self.log( "Reprinting elements..." )
         
         if self.cursesWindow:
            self.printElements( self.screen, self.cursesWindow )
         else:
            self.printElements( self.screen )
         
         self.isRefreshing = False
      self.logEnd()
   
   def recursivePrintElements( self, element : object, lineCounter : int = 0, charCounter : int = 0, win : object = None ):
      
      self.log( "{o}: text: {t} color: {c}".format( o=element.getClassName(), t=element.text, c=str( element.color ) ) )
      
      if element.text:
         if win:
            win.addString( lineCounter, charCounter, element.text, element.color )
         charCounter += len(element.text)
      
      for child in element.getChildren():
         lineCounter, charCounter = self.recursivePrintElements( child, lineCounter, charCounter, win )
      
      if element.isEndingLine:
         charCounter = 0
         lineCounter += 1
         
      return lineCounter, charCounter
   
   def printElements( self, screen, win = None ):
      self.logStart( "cursesWindow: {win}".format( win=bool(win) ) )
      if win:
         self.log("clearing curses window")
         win.clear()
      
      self.log("printing elements")
      try:
         self.recursivePrintElements( screen, 0, 0, win )
      except Exception as e:
         # screen might be full
         self.logError("Exception caught '{ex}'".format( ex=e ))
      
      if win:
         self.log("refreshing curses window")
         win.refresh()
      self.logEnd()
      
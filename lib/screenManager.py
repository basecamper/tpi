from lib.glob import Global, GlobalRuntime
from lib.log import Log
from lib.cursesWindow import CursesWindow
from lib.screen.overview import Overview
from lib.screen.screenColor import Color


class ScreenManager( Log ):
   
   def __init__( self ):
      Log.__init__( self, className="ScreenManager" )
      self.cursesWindow = CursesWindow() if not Global.DEBUG else None
      self.screen = Overview()
      self.isRefreshing = False
   
   def __del__( self ):
      del( self.cursesWindow )
      del( self.screen )
      del( self )
   
   def onButtonDown( self, button ):
      if not self.screen.propagateExclusiveButtonDown( button ):
         self.screen.onButtonDown( button )
      self.run() # be very responsive
   
   def run( self, evalReturn = True ):
      if not self.isRefreshing and GlobalRuntime.refreshScreen:
         self.isRefreshing = True
         
         self.screen.run()
         
         if not Log.wasStatusChecked():
            raise Exception("ScreenManager.run() latest status wasn't checked - make sure to Log.pop in a parent screenElement after all status are set")
         
         if self.cursesWindow:
            self.printElements( self.screen, self.cursesWindow )
         else:
            self.printElements( self.screen )
            
         self.isRefreshing = False
   
   
   def recursivePrintElements( self, element : object, lineCounter : int = 0, charCounter : int = 0, win : object = None ):
      # self.logStart( "recursivePrintElements", "line: {l} char: {ch} text: {t} {col} ({colv}) children {clen}{e}".format(
      #    l=lineCounter,
      #    ch=charCounter,
      #    t=element.text,
      #    col=element.color,
      #    colv=element.color.value,
      #    clen=len(element.getChildren()),
      #    e=" - LINEEND" if element.isEndingLine else "") )
      
      if element.text:
         if win:
            win.addString( lineCounter, charCounter, element.text, element.color )
         charCounter += len(element.text)
      
      for child in element.getChildren():
         lineCounter, charCounter = self.recursivePrintElements( child, lineCounter, charCounter, win )
      
      
      if element.isEndingLine:
         # self.log( message="line: {l} char: {c} - LINEENDING".format( l=lineCounter, c=charCounter ) )
         charCounter = 0
         lineCounter += 1
      
      # self.logEnd( printMessage=False )      
      return lineCounter, charCounter
   
   def printElements( self, screen, win = None ):
      self.logStart( "printElements","cursesWindow: {win}".format( win=bool(win) ) )
      if win:
         self.log("clearing curses window")
         win.clear()
      
      self.log("printing elements")
      self.recursivePrintElements( screen, 0, 0, win )
      
      if win:
         self.log("refreshing curses window")
         win.refresh()
      self.logEnd()
      
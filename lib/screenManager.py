from lib.screen.screenColor import Color
from lib.glob import Global, GlobalRuntime
from lib.log import Log
from lib.cursesWindow import CursesWindow
from lib.screen.view import Overview



class ScreenManager():
   def __init__( self ):
      self.cursesWindow = CursesWindow() if not Global.DEBUG else None
      self.screen = Overview()
      self.isRefreshing = False
   
   def onButtonDown( self, button ):
      self.screen.onButtonDown( button )
      self.run() # be very responsive
   
   def run( self, evalReturn = True ):
      if not self.isRefreshing and not GlobalRuntime.lockScreen:
         self.isRefreshing = True
         
         self.screen.run()
         
         if self.cursesWindow:
            ScreenManager.printElements( self.screen, self.cursesWindow )
         else:
            ScreenManager.printElements( self.screen )
            
         self.isRefreshing = False
   
   
   @staticmethod
   def recursivePrintElements( element : object, lineCounter : int = 0, charCounter : int = 0, win : object = None ):
      Log.debug( "line {char} char {char} text '{text}' {color} {colorValue} children {clen}".format(
         line=lineCounter,
         char=charCounter,
         text=element.text,
         color=element.color,
         colorValue=element.color.value,
         clen=len(element.getChildren()) ) )
      
      if element.text:
         if win:
            win.addString( lineCounter, charCounter, element.text, element.color )
         charCounter += len(element.text)
      
      for child in element.getChildren():
         lineCounter, charCounter = ScreenManager.recursivePrintElements( child, lineCounter, charCounter, win )
      
      if element.isEndingLine:
         Log.debug("endline {chars} chars".format(chars=charCounter))
         charCounter = 0
         lineCounter += 1
      
      return lineCounter, charCounter
   
   @staticmethod
   def printElements( screen, win = None ):
      if win:
         win.clear()
      ScreenManager.recursivePrintElements( screen, 0, 0, win )
      if win:
         win.refresh()
      
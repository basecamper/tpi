import curses
from lib.screen.screenColor import Color
from time import sleep
class CursesWindow:
   def __init__( self ):
      self.stdscr = curses.initscr()
      curses.nocbreak()
      self.stdscr.keypad(False)
      curses.noecho()
      curses.curs_set(0)
      curses.start_color()
      curses.init_pair(Color.GREEN.value, curses.COLOR_GREEN, curses.COLOR_BLACK)
      curses.init_pair(Color.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_BLACK)
      curses.init_pair(Color.RED.value, curses.COLOR_RED, curses.COLOR_BLACK)
      curses.init_pair(Color.BLACKWHITE.value, curses.COLOR_BLACK, curses.COLOR_WHITE)
      
   def __del__( self ):
      time.sleep(10)
      curses.nocbreak()
      self.stdscr.keypad(False)
      curses.echo()
      curses.endwin()
   
   def clear( self ):
      self.stdscr.clear()
      
   def refresh( self ):
      self.stdscr.refresh()
      
   def addString( self, line, char, text, color ):
      self.stdscr.addstr( line, char, text, curses.color_pair( color.value ) )
      
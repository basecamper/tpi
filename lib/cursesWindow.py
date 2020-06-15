import curses
from time import sleep

from lib.screen.screenColor import Color
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
      self.stdscr.keypad(True)
      curses.echo()
      curses.curs_set(1)
      curses.endwin()
      del( self.stdscr )
   
   def clear( self ):
      self.stdscr.clear()
      
   def refresh( self ):
      self.stdscr.refresh()
      
   def addString( self, line, char, text, color ):
      self.stdscr.addstr( line, char, text, curses.color_pair( color.value ) )
      
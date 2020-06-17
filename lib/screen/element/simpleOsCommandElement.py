from lib.procHandler import ProcHandler
from lib.hasStep import HasStep
from lib.log import Log
from lib.screen.screenColor import Color
from lib.screen.element import ScreenElement
from lib.screen.element.pollingElement import PollingElement

STEP_IDLE = 0
STEP_START = 1
STEP_STARTED = 2
STEP_FINISHED = 3
STEP_CONFIRM_RESULT = 4
STEP_CLEANUP = 5
   
TEXT_ERROR = "error"
TEXT_OK = "ok"
COLOR_ERROR = Color.RED
COLOR_OK = Color.GREEN

class SimpleOsCommandElement( ScreenElement, HasStep, Log ):
   
   def __init__( self,
                 text : str,
                 button : object,
                 command : list,
                 cooldown : int = 0,
                 timeout : int = 3,
                 callback : object = None ):
      
      ScreenElement.__init__( self, buttonProcMap={ button : self.onButtonDown } )
      HasStep.__init__( self, STEP_IDLE )
      Log.__init__( self, "SimpleOsCommandElement" )
      
      self._commandText = text
      self._button = button
      self._command = command
      self._parentCallback = callback
      self._procHandler = ProcHandler( command=command,
                                       fullCallback=self.onProcessFinished,
                                       cooldown=cooldown,
                                       timeout=timeout )
      self._finishedProcess = None
      self._dataElement = ScreenElement()
      self.addChild( self._dataElement )
      self._resetText()
   
   def run( self ):
      self.logStart("run")
      
      # command text is shown wait for button press
      if self.hasStep( STEP_IDLE ):
         pass
      
      # button pressed, start subprocess
      if self.hasStep( STEP_START ):
         self._procHandler.run()
         self.setStep( STEP_STARTED )
      
      # wait in step started for the process to finish
      if self.hasStep( STEP_STARTED ):
         pass
      
      # process finished, evaluate return value of self._finishedProcess
      if self.hasStep( STEP_FINISHED ):
         if self._evalFinishedProcessReturnValue():
            self._setDataElement( TEXT_OK, COLOR_OK )
         else:
            self._setDataElement( TEXT_ERROR, COLOR_ERROR )
         self.setStep( STEP_CONFIRM_RESULT )
      
      # show ok/error until button is pressed
      if self.hasStep( STEP_CONFIRM_RESULT ):
         pass
      
      # button pressed, reset command text
      if self.hasStep( STEP_CLEANUP ):
         self._resetText()
         self.setStep( STEP_IDLE )
      
      self.logEnd()
   
   def onButtonDown( self, button ):
      if self.hasStep( STEP_IDLE ):
         self.setStep( STEP_START )
      if self.hasStep( STEP_CONFIRM_RESULT ):
         self.setStep( STEP_CLEANUP )
   
   def onProcessFinished( self, proc ):
      self._finishedProcess = proc
      self.setStep( STEP_FINISHED )
   
   def _evalFinishedProcessReturnValue( self, proc ):
      return self._finishedProcess and not self._finishedProcess.returnValue > 0
   
   def _setDataElement( self, text : str, color : object = Color.DEFAULT ):
      self._dataElement.text, self._dataElement.color = text, color
   
   def _resetText( self ):
      self._setDataElement( text=self._commandText )

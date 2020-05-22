from lib.screen import ScreenElement
class Menu( ScreenElement ):
   def __init__( self, menuItems : list, nextButton : object, prevButton : object ):
      super().__init__()
      self.container = ScreenElement()
      self.addChild( self.container )
      self.menuItems = menuItems
      self.nextButton = nextButton
      self.prevButton = prevButton
      self.itemIndex = 0
      self.container.addChild( self.menuItems[0] )
   
   def onButtonDown( self, button ):
      if button == self.nextButton and self.itemIndex < len( self.menuItems ) - 1:
         self.itemIndex += 1
         self.container.emptyChildren()
         self.container.addChild( self.menuItems[ self.itemIndex ] )
      elif button == self.prevButton and self.itemIndex > 0:
         self.itemIndex -= 1
         self.container.emptyChildren()
         self.container.addChild( self.menuItems[ self.itemIndex ] )
      else:
         self.menuItems[ self.itemIndex ].onButtonDown( button )
      super().run()
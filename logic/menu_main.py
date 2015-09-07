import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from menu_game import MenuGame
from ui.frame_main_menu import FrameMainMenu

class MenuMain(Menu):

	def __init__(self, width, height):
		Menu.__init__(self, width, height)
		self.menu_frame = FrameMainMenu(width, height)

	def update(self, delta):
		self.menu_frame.update(delta)

		key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress
		if key.c == ord("a"):
			return MenuGame(self.width, self.height)
		if key.c == ord("b"):
			return MenuStatus.Exit

		return MenuStatus.Okay

	def draw(self):
		#print("drawing MenuMain")
		self.menu_frame.draw()
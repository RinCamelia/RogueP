import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from menu_game import MenuGame

class MenuMain(Menu):

	def __init__(self, width, height):
		Menu.__init__(self, width, height)
		self.text_base = width/2, height/4
		self.title_text = "ROGUEP: A Game of Viruses"
		self.option_one_text = "Play"
		self.option_two_text = "Quit"

	def update(self, delta):
		key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress

		if key.c == ord("a"):
			return MenuGame(self.width, self.height)

		if key.c == ord("b"):
			return MenuStatus.Exit

		return MenuStatus.Okay

	def draw(self):
		#print("drawing MenuMain")
		libtcod.console_set_alignment(0, libtcod.CENTER)
		libtcod.console_print(0, self.text_base[0], self.text_base[1], self.title_text)
		libtcod.console_print(0, self.text_base[0], self.text_base[1] + 2, "a  " + self.option_one_text)
		libtcod.console_print(0, self.text_base[0], self.text_base[1] + 4, "b  " + self.option_two_text)
		libtcod.console_flush()
		libtcod.console_clear(0)
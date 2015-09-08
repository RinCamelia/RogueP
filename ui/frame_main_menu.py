import libtcodpy as libtcod
from frame import Frame

class FrameMainMenu(Frame):

	def __init__(self, root_console_width, root_console_height, frame_manager=None):
		Frame.__init__(self, root_console_width, root_console_height, frame_manager)
		self.text_base = root_console_width/2, root_console_height/4
		self.title_text = "ROGUEP: A Game of Viruses"
		self.option_one_text = "Play"
		self.option_two_text = "Quit"

	def draw(self):
		libtcod.console_set_alignment(0, libtcod.CENTER)
		libtcod.console_print(0, self.text_base[0], self.text_base[1], self.title_text)
		libtcod.console_print(0, self.text_base[0], self.text_base[1] + 2, "a  " + self.option_one_text)
		libtcod.console_print(0, self.text_base[0], self.text_base[1] + 4, "b  " + self.option_two_text)
		libtcod.console_flush()
		libtcod.console_clear(0)
# a frame class that holds its own offscreen console for the purposes of drawing a UI panel or element on screen

import libtcodpy as libtcod

class Frame:

	def __init__(self, root_console_width, root_console_height, width=0, height=0):
		self.root_console_height = root_console_width
		self.root_console_height = root_console_height

		self.width = width
		self.height = height

		if width > 0 and height > 0:
			self.console = libtcod.console_new(width, height)

	def update(self, delta):
		pass

	def handle_ui_event(self, key):
		pass

	def draw(self):
		pass


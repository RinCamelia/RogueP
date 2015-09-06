# a frame class that holds its own offscreen console for the purposes of drawing a UI panel or element on screen

import libtcodpy as libtcod

class Frame:

	def __init__(self, console_width, console_height):
		self.console_width = console_width
		self.console_height = console_height

	def update(self, delta):
		pass

	def handle_ui_event(self, key):
		pass

	def draw(self):
		pass


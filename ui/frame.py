# a frame class that holds its own offscreen console for the purposes of drawing a UI panel or element on screen

import libtcodpy as libtcod

class Frame:

	def __init__(self, width, height):
		self.width = width
		self.height = height

	def update(self, delta):
		pass

	def handle_key_input(self, key):
		pass

	def draw(self):
		pass


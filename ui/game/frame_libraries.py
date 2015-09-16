# added specifically to make floating point division apply to code in bar position calculation
from __future__ import division

import libtcodpy as libtcod
import xp_loader
import gzip
from vec2d import Vec2d

from ui.frame import Frame
from ui.ui_event import UIEvent, UIEventType

# Displays remaining and queued actions. 
class FrameLibraries(Frame):

	def __init__(self, root_console_width, root_console_height, frame_manager):
		self.entity_manager = frame_manager.parent_menu.entity_manager

		# load xp for bg
		console_bg_xp = gzip.open('assets\\ui\\ui_frame_libraries_bg.xp')
		self.bg_data = xp_loader.load_xp_string(console_bg_xp.read())

		Frame.__init__(self, root_console_width, root_console_height, self.bg_data['width'], self.bg_data['height'], frame_manager)


		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

	def handle_ui_event(self, event):
		pass

	def draw(self):

		libtcod.console_clear(self.console)
		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
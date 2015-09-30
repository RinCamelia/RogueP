# added specifically to make floating point division apply to code in bar position calculation
from __future__ import division

import libtcodpy as libtcod
import xp_loader
import gzip
from vec2d import Vec2d

from model.attribute import AttributeTag

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

		library_start_xy = xp_loader.get_position_key_xy(self.bg_data['layer_data'][1], xp_loader.poskey_color_red)

		self.library_start_xy = Vec2d(library_start_xy[0], library_start_xy[1])
		self.library_line_extent = xp_loader.get_position_key_xy(self.bg_data['layer_data'][1], xp_loader.poskey_color_green)

		#TODO put these in config somewhere
		self.line_char = chr(196)
		self.line_bg = libtcod.Color(2, 22, 12)
		self.line_fg = libtcod.Color(6, 130, 60)
		self.libname_fg = libtcod.Color(102, 255, 178)

		libtcod.console_set_default_background(self.console,self.line_bg)
		libtcod.console_set_default_foreground(self.console,self.libname_fg)
		libtcod.console_set_alignment(self.console, libtcod.LEFT)

		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

	def handle_ui_event(self, event):
		pass

	def draw(self):

		libtcod.console_clear(self.console)
		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

		player_libraries = self.entity_manager.get_entity_by_id(self.entity_manager.player_id).get_attribute(AttributeTag.Libraries).data['value']

		for lib in range(4):
			#+1 here because range will go up to but not including the final screen tile needed
			for x in range(self.library_line_extent[0] - self.library_start_xy[0] + 1):
				libtcod.console_put_char_ex(self.console, self.library_start_xy[0] + x, self.library_start_xy[1] + lib, self.line_char, self.line_fg, self.line_bg)
			libname_xy = Vec2d(self.library_start_xy[0], self.library_start_xy[1] + lib)
			#TODO: move to config strings
			libname = 'lib_missing'
			print_color = self.line_fg

			if len(player_libraries) > lib:
				print_color = self.libname_fg
				libname = player_libraries[lib].name

			libtcod.console_set_default_foreground(self.console, print_color)
			libtcod.console_print(self.console, libname_xy[0], libname_xy[1], libname)

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
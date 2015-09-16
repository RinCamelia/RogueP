# added specifically to make floating point division apply to code in bar position calculation
from __future__ import division

import libtcodpy as libtcod
import xp_loader
import gzip
from vec2d import Vec2d

from ui.strings.command_responses import command_response_table
from ui.frame import Frame
from ui.ui_event import UIEvent, UIEventType

# commands frame - displays a background and manages creating and destroying informational other input related frames
class FrameCommands(Frame):

	def __init__(self, root_console_width, root_console_height, start_x, frame_height, frame_manager):
		#TODO make and load .XP file with background, and arrange it to have an autoextending background
		Frame.__init__(self, root_console_width, root_console_height, root_console_width - start_x, frame_height, frame_manager)
		self.start_x = start_x


	def update(self, delta):
		pass


	def handle_ui_event(self, event):
		pass

	def draw(self):
		libtcod.console_clear(self.console)
		libtcod.console_hline(self.console, 0, 0, self.width)

		libtcod.console_set_alignment(self.console, libtcod.LEFT)
		libtcod.console_print(self.console, 0, 0, "COMMANDS")

		libtcod.console_hline(self.console, 0, self.height - 1, self.width)
		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, self.start_x, 0)


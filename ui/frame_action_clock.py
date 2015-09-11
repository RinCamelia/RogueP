# added specifically to make floating point division apply to code in bar position calculation
from __future__ import division

import libtcodpy as libtcod
import xp_loader
import gzip
from vec2d import Vec2d

from frame import Frame
from ui_event import UIEvent, UIEventType

# Displays remaining and queued actions. 
class FrameActionClock(Frame):

	def __init__(self, root_console_width, root_console_height, frame_manager):
		# constants and initialization
		self.current_action_count = 0
		self.max_actions = 0
		self.highlighted_tile_count = 0
		self.entity_manager = frame_manager.parent_menu.entity_manager

		# load xp for bg
		console_bg_xp = gzip.open('assets\\ui\\ui_frame_actionclock_bg.xp')
		self.bg_data = xp_loader.load_xp_string(console_bg_xp.read())

		Frame.__init__(self, root_console_width, root_console_height, self.bg_data['width'], self.bg_data['height'], frame_manager)


		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

		queued_actions_display_start = None
		queued_actions_display_end = None

		#scrape the xp file for position markers for action clock bar and text for actions remaining
		x = 0
		for row in self.bg_data['layer_data'][1]['cells']:
			y = 0
			for cell in row:
				if cell['fore_r'] == 255 and cell['fore_g'] == 0 and cell['fore_b'] == 0:
					self.remaining_actions_display_position = Vec2d(x, y)
				elif cell['fore_r'] == 255 and cell['fore_g'] == 255 and cell['fore_b'] == 0:
					queued_actions_display_start = Vec2d(x, y)
				elif cell['fore_r'] == 0 and cell['fore_g'] == 255 and cell['fore_b'] == 0:
					queued_actions_display_end = Vec2d(x, y)
				y += 1
			x += 1

		self.queued_actions_display_start = queued_actions_display_start
		self.queued_actions_bar_width = queued_actions_display_end[0] - queued_actions_display_start[0]

	def handle_ui_event(self, event):
		if event.type == UIEventType.ActionQueueAdd:
			self.current_action_count += event.data['action'].data['cost']
		elif event.type == UIEventType.ActionQueueClear:
			self.current_action_count = 0
		elif event.type == UIEventType.ActionQueueMaxActionsChange:
			self.max_actions = event.data['max_actions']
		percent_queued = self.current_action_count / self.max_actions
		self.highlighted_tile_count = round(percent_queued * self.queued_actions_bar_width)


	def draw(self):

		libtcod.console_clear(self.console)
		xp_loader.load_layer_to_console(self.console, self.bg_data['layer_data'][0])

		libtcod.console_set_alignment(self.console, libtcod.LEFT)
		libtcod.console_print(self.console, self.remaining_actions_display_position[0], self.remaining_actions_display_position[1], str(self.max_actions - self.current_action_count))

		for x in range(self.queued_actions_bar_width + 1):
			if x <= self.highlighted_tile_count and self.highlighted_tile_count > 0:
				libtcod.console_put_char(self.console, self.queued_actions_display_start[0] + x, self.queued_actions_display_start[1], chr(178))
			else:
				libtcod.console_put_char(self.console, self.queued_actions_display_start[0] + x, self.queued_actions_display_start[1], chr(176))

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
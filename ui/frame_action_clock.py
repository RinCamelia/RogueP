import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from objects.event import Event, EventTag
from frame import Frame
from vec2d import Vec2d
from frame_manager import FrameState
import xp_loader
import gzip

# UI drawing class for the actual game world, renders to the subset of the screen that is not UI
# or will, anyway, just draws right to the console atm
class FrameActionClock(Frame):

	def __init__(self, console_width, console_height, entity_manager):
		Frame.__init__(self, console_width, console_height)
		self.entity_manager = entity_manager
		console_bg_xp = gzip.open('assets\\ui\\ui_frame_actionclock_bg.xp')
		bg_parsed = xp_loader.load_xp_string(console_bg_xp.read())
		self.console = libtcod.console_new(bg_parsed['width'], bg_parsed['height'])
		self.width = bg_parsed['width']
		self.height = bg_parsed['height']
		xp_loader.load_layer_to_console(self.console, bg_parsed['layer_data'][0])
		x = 0
		for row in bg_parsed['layer_data'][1]['cells']:
			y = 0
			for cell in row:
				if cell['fore_r'] == 255 and cell['fore_g'] == 0 and cell['fore_b'] == 0:
					self.remaining_actions_display_position = Vec2d(x, y)
				elif cell['fore_r'] == 255 and cell['fore_g'] == 255 and cell['fore_b'] == 0:
					self.queued_actions_display_position = Vec2d(x, y)
				y += 1
			x += 1

	def update(self, delta):
		pass

	def draw(self):
		libtcod.console_put_char(self.console, self.remaining_actions_display_position[0], self.remaining_actions_display_position[1], '1')
		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
		libtcod.console_put_char(self.console, self.remaining_actions_display_position[0], self.remaining_actions_display_position[1], ' ')

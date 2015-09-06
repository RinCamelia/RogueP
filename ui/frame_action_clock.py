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

	def update(self, delta):
		pass

	def draw(self):
		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
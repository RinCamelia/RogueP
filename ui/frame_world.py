import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from objects.event import Event, EventTag
from frame import Frame
from frame_manager import FrameState

# UI drawing class for the actual game world, renders to the subset of the screen that is not UI
# or will, anyway, just draws right to the console atm
class FrameWorld(Frame):

	def __init__(self, width, height, entity_manager):
		Frame.__init__(self, width, height)
		self.entity_manager = entity_manager

	def update(self, delta):
		# may need update logic, for now, nothing
		pass

	def draw(self):
		clear_entities = []
		libtcod.console_clear(0)
		for entity in self.entity_manager.entities:
			if entity.get_attribute(AttributeTag.Visible):
				draw_info = entity.get_attribute(AttributeTag.CharacterDrawInfo)
				position_info = entity.get_attribute(AttributeTag.WorldPosition).data['value']
				if not draw_info or not position_info:
					raise LookupError
				libtcod.console_put_char(0, position_info.x, position_info.y, chr(draw_info.data['character']), libtcod.BKGND_NONE)
		libtcod.console_flush()

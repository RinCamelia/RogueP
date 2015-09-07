import libtcodpy as libtcod
from logic.menu import Menu
from logic.menu_manager import MenuStatus
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from model.action import Action, ActionTag
from frame import Frame
from vec2d import Vec2d
from ui_event import UIEvent, UIEventType
from frame_manager import FrameState

# UI drawing class for the actual game world, renders to the subset of the screen that is not UI
# or will, anyway, just draws right to the console atm
# right now scrapes game state directly to draw things - may (and probably will) in the future harvest UI events to update the UI (pulling info only when player scans, etc)
class FrameActionsOverlay(Frame):

	def __init__(self, root_console_width, root_console_height, entity_manager):
		Frame.__init__(self, root_console_width, root_console_height, root_console_width, root_console_height)
		self.entity_manager = entity_manager
		self.actions = []
		libtcod.console_set_default_background(self.console, libtcod.Color(255, 0, 255))
		libtcod.console_set_key_color(self.console, libtcod.Color(255, 0, 255))

	def update(self, delta):
		# may need update logic, for now, nothing
		pass

	def handle_ui_event(self, event):
		if event.type == UIEventType.ActionQueueAdd:
			self.actions.append(event.data['action'])
		if event.type == UIEventType.ActionQueueRemove:
			self.actions.remove(event.data['action'])
		elif event.type == UIEventType.ActionQueueClear:
			self.actions = []

	#is mostly temporary proof of concept
	def draw(self):
		libtcod.console_clear(self.console)
		player = filter(lambda ent: ent.get_attribute(AttributeTag.Player), self.entity_manager.entities)[0]
		player_position = player.get_attribute(AttributeTag.WorldPosition).data['value']
		position_delta = Vec2d(0, 0)

		for queued_action in self.actions:
			position_delta += queued_action.data['value']
			draw_info = player.get_attribute(AttributeTag.DrawInfo)
			target_position = player_position + position_delta
			libtcod.console_put_char_ex(self.console, target_position.x, target_position.y, chr(draw_info.data['character']), libtcod.grey, libtcod.black)

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
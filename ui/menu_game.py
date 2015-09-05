import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from behavior_manager import EntityManager
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from objects.event import Event, EventTag
from frame_manager import FrameManager
from frame_world import FrameWorld
from vec2d import Vec2d

class MenuGame(Menu):

	def __init__(self, width, height):
		Menu.__init__(self, width, height)
		#currently hardcoded to test player movement
		self.behavior_manager = EntityManager()
		self.frame_manager = FrameManager()
		world_frame = FrameWorld(width, height, self.behavior_manager)
		self.frame_manager.add_frame(world_frame)
		self.behavior_manager.add_entity(Entity([
					Attribute(AttributeTag.Player),
					Attribute(AttributeTag.Visible),
					Attribute(AttributeTag.WorldPosition, {'value': Vec2d(20, 20)}),
					Attribute(AttributeTag.MaxProgramSize, {'value': 20}),
					Attribute(AttributeTag.DrawInfo, {'character': 64, 'draw_func': FrameWorld.draw_entity_as_character})
				])
			)

	def update(self, delta):
		key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress

		if key.vk == libtcod.KEY_UP:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {'value': Vec2d(0, -1)}))

		if key.vk == libtcod.KEY_DOWN:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {'value': Vec2d(0, 1)}))

		if key.vk == libtcod.KEY_LEFT:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {'value': Vec2d(-1, 0)}))

		if key.vk == libtcod.KEY_RIGHT:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {'value': Vec2d(1, 0)}))

		self.behavior_manager.update_behaviors(delta)
		self.frame_manager.update(delta)

		if key.c == ord("q"):
			return MenuStatus.Exit
			
		return MenuStatus.Okay

	def draw(self):
		self.frame_manager.draw()
		pass
import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from behavior_manager import BehaviorManager
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from objects.event import Event, EventTag

class MenuGame(Menu):

	def __init__(self, width, height):
		Menu.__init__(self, width, height)
		#currently hardcoded to test player movement
		self.behavior_manager = BehaviorManager()
		self.entities = []
		self.entities.append(
			Entity([
					Attribute(AttributeTag.Player),
					Attribute(AttributeTag.Visible),
					Attribute(AttributeTag.WorldPosition, {'x': 20, 'y': 20}),
					Attribute(AttributeTag.CharacterDrawInfo, {'character': '@'})
				])
			)
		self.last_key = libtcod.console_check_for_keypress(True)

	def update(self, delta):
		self.last_key = self.current_key
	    self.current_key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress

		if key.c == ord("q"):
			print("should be escaping")
			return MenuStatus.Exit
		

		if key.vk == libtcod.KEY_UP:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {"x": 0, "y": -1}), self.entities)

		if key.vk == libtcod.KEY_DOWN:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {"x": 0, "y": 1}), self.entities)

		if key.vk == libtcod.KEY_LEFT:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {"x": -1, "y": 0}), self.entities)

		if key.vk == libtcod.KEY_RIGHT:
			self.behavior_manager.handle_event(Event(EventTag.PlayerMovement, {"x": 1, "y": 0}), self.entities)

		self.behavior_manager.update_behaviors(self.entities)
		return MenuStatus.Okay

	def draw(self):
		#print("drawing MenuGame")
		pass
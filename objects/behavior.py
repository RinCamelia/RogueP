import libtcodpy as libtcod
import entity, attribute

class Behavior:
	def __init__(self, manager):
		self.manager = manager

	def apply_to_entity(self, entity):
		pass

	def apply_to_all_entities(self, entities):
		pass

	def handle_event(self, event, entities):
		pass



class PlayerMovementBehavior(Behavior):

	def handle_event(self, event, entities):
		for entity in entities:
			if entity.get_attribute(attribute.AttributeTag.Player):
				self.update_player_pos(entity.get_attribute(attribute.AttributeTag.WorldPosition), event.data)

	def update_player_pos(self, player_position, position_delta):
		player_position.data["x"] += position_delta["x"]
		player_position.data["y"] += position_delta["y"]

class DrawBehavior(Behavior):

	def apply_to_all_entities(self, entities):
		libtcod.console_set_default_foreground(0, libtcod.white)
		for entity in entities:
			if entity.get_attribute(attribute.AttributeTag.Visible):
				draw_info = entity.get_attribute(attribute.AttributeTag.CharacterDrawInfo)
				position_info = entity.get_attribute(attribute.AttributeTag.WorldPosition)
				if not draw_info or not position_info:
					raise LookupError
				libtcod.console_put_char(0, position_info.data["x"], position_info.data["y"], draw_info.data["character"], libtcod.BKGND_NONE)
				libtcod.console_flush()
				libtcod.console_put_char(0, position_info.data["x"], position_info.data["y"], ' ', libtcod.BKGND_NONE)
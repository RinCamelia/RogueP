import libtcodpy as libtcod
from vec2d import Vec2d
from action import ActionTag
from attribute import Attribute, AttributeTag
from entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld

class Behavior:
	def __init__(self, manager):
		self.manager = manager

	def apply_to_entity(self, entity):
		pass

	def apply_to_all_entities(self):
		pass

	def handle_action(self, action):
		pass

def is_player_memory(player, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == player.id:
		return True
	return False


# TODO: pull this code out into a more generic one for programs
class PlayerMovementBehavior(Behavior):

	def handle_action(self, action):
		if action.type == ActionTag.PlayerMovement:
			player = filter(lambda ent:ent.get_attribute(AttributeTag.Player), self.manager.entities)[0]
			player_position = player.get_attribute(AttributeTag.WorldPosition)
			new_player_position = player_position.data['value'] + action.data['value']
			# TODO make it check the parent program

			player_program_squares = filter(lambda ent: is_player_memory(player, ent), self.manager.entities)

			# -1 here because the player's actual character position counts for purposes of max memory size
			if len(player_program_squares) >= player.get_attribute(AttributeTag.MaxProgramSize).data['value'] - 1:
				remove_square_id = -1
				#remove either the oldest memory segment, or the memory segment the player is moving onto
				for mem in player_program_squares:
					if new_player_position.get_distance(mem.get_attribute(AttributeTag.WorldPosition).data['value']) == 0:
						remove_square_id = mem.id
						break
					if mem.id < remove_square_id or remove_square_id == -1:
						remove_square_id = mem.id

				self.manager.remove_entity_by_id(remove_square_id)
			self.manager.add_entity(Entity([
					Attribute(AttributeTag.ProgramMemory, {'parent_id': player.id}),
					Attribute(AttributeTag.Visible),
					Attribute(AttributeTag.WorldPosition, {'value': player_position.data['value']}),
				]))

			player_position.data['value'] = new_player_position

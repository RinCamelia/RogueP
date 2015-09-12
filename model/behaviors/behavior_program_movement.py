import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import Action, ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld
from behavior import Behavior
from model.entity_utilities import *

# TODO: pull this code out into a more generic one for programs
class ProgramMovementBehavior(Behavior):
	def handle_action(self, action):
		actions = []
		if action.type == ActionTag.ProgramMovement:
			program = self.manager.get_entity_by_id(action.data['target_id'])

			position_delta = action.data['value']
			new_position = program.get_attribute(AttributeTag.WorldPosition).data['value'] + position_delta

			existing_memory = filter(lambda ent: is_owned_memory(program.id, ent), self.manager.entities)
			entities_at_new_position = self.manager.get_entities_by_position(new_position)

			if position_delta[0] < -1 or position_delta[0] > 1 or position_delta[1] < -1 or position_delta [1] > 1 or (position_delta[0] != 0 and position_delta[1] != 0):
				raise ValueError('Attempted to process a ProgramMovement action with invalid movement parameters ' + position_delta)

			if not entities_occupy_position(program.id, entities_at_new_position) and position_delta != Vec2d(0, 0):
				# -1 here because the program itself counts for purposes of max memory size
				if len(existing_memory) >= program.get_attribute(AttributeTag.MaxProgramSize).data['value'] - 1:

					#todo: possibly split this into a 'ProgramMemoryCheckSegments' behavior that properly culls and regenerates the segments, and leave this for position stuff
					if len(filter(lambda ent: is_owned_memory(program.id, ent), entities_at_new_position)) == 0:
						existing_memory.sort(lambda ent,other: cmp(ent.id, other.id))
						actions.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position':existing_memory[0].get_attribute(AttributeTag.WorldPosition).data['value']}))
					else:
						actions.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position': new_position}))

				actions.append(Action(ActionTag.ProgramMemoryAdd, {'parent_id': program.id, 'position': program.get_attribute(AttributeTag.WorldPosition).data['value']}))
				program.get_attribute(AttributeTag.WorldPosition).data['value'] = new_position
		return actions
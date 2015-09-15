import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import Action, ActionTag
from model.attribute import AttributeTag
from behavior import Behavior

#note: an explicit from [] import * because if I don't, using entity_utilities functions in lambdas throws a fit
from model.entity_utilities import *

# TODO: pull this code out into a more generic one for programs
class ProgramMovementBehavior(Behavior):
	def handle_action(self, action):
		actions = []
		if action.type == ActionTag.ProgramMovement:
			program = self.manager.get_entity_by_id(action.data['target_id'])
			old_position = program.get_attribute(AttributeTag.WorldPosition).data['value']
			position_delta = action.data['value']
			new_position = old_position + position_delta

			existing_memory = program.get_attribute(AttributeTag.OwnedMemory).data['segments']
			new_position_world_data = self.manager.get_world_data_for_position(new_position)

			if position_delta[0] < -1 or position_delta[0] > 1 or position_delta[1] < -1 or position_delta [1] > 1 or (position_delta[0] != 0 and position_delta[1] != 0):
				raise ValueError('Attempted to process a ProgramMovement action with invalid movement parameters ' + str(position_delta))

			if not entities_occupy_position(program.id, new_position_world_data) and position_delta != Vec2d(0, 0):
				# -1 here because the program itself counts for purposes of max memory size
				if len(filter(lambda ent: is_owned_memory(program.id, ent),  new_position_world_data['entities'])) > 0:
					actions.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position': new_position}))
				elif len(existing_memory) >= program.get_attribute(AttributeTag.MaxProgramSize).data['value'] - 1:
					existing_memory.sort(lambda ent,other: cmp(ent.id, other.id))
					actions.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position':existing_memory[0].get_attribute(AttributeTag.WorldPosition).data['value']}))

				actions.append(Action(ActionTag.ProgramMemoryAdd, {'parent_id': program.id, 'position': program.get_attribute(AttributeTag.WorldPosition).data['value']}))

				# update the manager's world tile data to consistency with the move we're doing
				self.manager.world_tiles[old_position[0]][old_position[1]]['entities'].remove(program)
				self.manager.world_tiles[new_position[0]][new_position[1]]['entities'].append(program)

				program.get_attribute(AttributeTag.WorldPosition).data['value'] = new_position
		return actions
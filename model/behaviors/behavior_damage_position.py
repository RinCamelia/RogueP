import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import Action, ActionTag
from model.attribute import Attribute, AttributeTag
from behavior import Behavior

#note: an explicit from [] import * because if I don't, using entity_utilities functions in lambdas throws a fit
from model.entity_utilities import *

# TODO: pull this code out into a more generic one for programs
class DamagePositionBehavior(Behavior):
	def handle_action(self, action):
		actions = []
		if action.type == ActionTag.DamagePosition:
			attacker = self.manager.get_entity_by_id(action.data['attacker_id'])
			position = None

			if 'relative' in action.data:
				position = attacker.get_attribute(AttributeTag.WorldPosition).data['value'] + action.data['relative']
			else:
				position = action.data['absolute']

			world_data_for_position = self.manager.get_world_data_for_position(position)

			for entity in filter(lambda ent: not is_owned_memory(attacker.id, ent), world_data_for_position['entities']):
				#really need introspection here to break the behavior out :/
				if is_program_main_segment(entity):
					#get and try to delete a random zeroed memory segment, if zeroed already, remove it
					#if not, zero a random memory segment
					owned_segments = entity.get_attribute(AttributeTag.OwnedMemory).data['segments']
					if len(owned_segments) == 0:
						actions.append(Action(ActionTag.ProgramMemoryRemove, 
							{'parent_id': entity.id, 'position': position}))
					else:
						owned_zeroed_segments = filter(lambda ent: ent.get_attribute(AttributeTag.Zeroed), owned_segments)
						if len(owned_zeroed_segments) == 0:
							segment = owned_segments[libtcod.random_get_int(0, 0, len(owned_segments) - 1)]
							segment.add_attribute(Attribute(AttributeTag.Zeroed))
						else:
							actions.append(Action(ActionTag.ProgramMemoryRemove, 
								{'parent_id': entity.id, 'position': position}))

				elif entity.get_attribute(AttributeTag.ProgramMemory):
					if not entity.get_attribute(AttributeTag.Zeroed):
						entity.add_attribute(Attribute(AttributeTag.Zeroed))
					else:
						actions.append(Action(ActionTag.ProgramMemoryRemove, 
							{'parent_id': entity.get_attribute(AttributeTag.ProgramMemory).data['parent_id'], 'position': position}))
				else:
					#???
					pass

		return actions
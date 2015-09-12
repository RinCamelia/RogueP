import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import Action, ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld
from behavior import Behavior

#yes, i know duplicate code, fast and ugly at the moment
#will make a pass tomorrow on evaluating a utility module versus raw filtering off manager versus functions on manager, and pick one to clean up the code
def is_memory_of_parent(parent_id, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == parent_id:
		return True
	return False

def is_hostile_memory(parent_id, ent):
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] != parent_id:
		return True
	return False


# TODO: pull this code out into a more generic one for programs
class ProgramMovementBehavior(Behavior):
	def handle_action(self, action):
		events = []
		if action.type == ActionTag.ProgramMovement:
			program = self.manager.get_entity_by_id(action.data['target_id'])

			position_delta = action.data['value']
			new_position = program.get_attribute(AttributeTag.WorldPosition).data['value'] + position_delta

			existing_memory = filter(lambda ent: is_memory_of_parent(program.id, ent), self.manager.entities)
			entities_at_new_position = self.manager.get_entities_by_position(new_position)

			if len(filter(lambda ent: ent.get_attribute(AttributeTag.HostileProgram) or is_hostile_memory(program.id, ent), entities_at_new_position)) == 0:
				# -1 here because the program itself counts for purposes of max memory size
				if len(existing_memory) >= program.get_attribute(AttributeTag.MaxProgramSize).data['value'] - 1:

					#todo: possibly split this into a 'ProgramMemoryCheckSegments' behavior that properly culls and regenerates the segments, and leave this for position stuff
					if len(filter(lambda ent: is_memory_of_parent(program.id, ent), entities_at_new_position)) == 0:
						existing_memory.sort(lambda ent,other: cmp(ent.id, other.id))
						events.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position':existing_memory[0].get_attribute(AttributeTag.WorldPosition).data['value']}))
					else:
						events.append(Action(ActionTag.ProgramMemoryRemove, {'parent_id': program.id, 'position': new_position}))

				events.append(Action(ActionTag.ProgramMemoryAdd, {'parent_id': program.id, 'position': program.get_attribute(AttributeTag.WorldPosition).data['value']}))
				program.get_attribute(AttributeTag.WorldPosition).data['value'] = new_position
		return events
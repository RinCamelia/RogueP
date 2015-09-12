import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld
from behavior import Behavior


def is_memory_of_parent(parent_id, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == parent_id:
		return True
	return False


# TODO: pull this code out into a more generic one for programs
class ProgramMemoryRemoveBehavior(Behavior):

	def remove_memory(self, parent, position):
		target_location_entities = filter(
			lambda ent: ent.get_attribute(AttributeTag.WorldPosition) 
					and ent.get_attribute(AttributeTag.WorldPosition).data['value'] == position
					and is_memory_of_parent(parent, ent), self.manager.entities)
		if len(target_location_entities) > 0:
			#will remove multiple copies of memory, best to be safe
			for entity in target_location_entities:
				self.manager.remove_entity_by_id(entity.id)


	def handle_action(self, action):
		if action.type == ActionTag.ProgramMemoryRemove:
			
			self.remove_memory(action.data['parent_id'], action.data['position'])
		return []


class ProgramMemoryAddBehavior(Behavior):
	def handle_action(self, action):
		if action.type == ActionTag.ProgramMemoryAdd:
			position = action.data['position']
			parent_id = action.data['parent_id']

			entities_at_location = self.manager.get_entities_by_position(position)

			#todo - break this into more general "is position empty/valid"
			if len(filter(lambda ent: not ent.get_attribute(AttributeTag.WorldTile), entities_at_location)) == 0:
				#todo - consider making this an explicit action instead of just chucking it into the manager? for now, this is fine
				self.manager.add_entity(Entity([
						Attribute(AttributeTag.ProgramMemory, {'parent_id': parent_id}),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.WorldPosition, {'value': position}),
					]))

		return []
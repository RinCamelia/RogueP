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
class AIRandomWalkBehavior(Behavior):
	def __init__(self, manager):
		Behavior.__init__(self, manager)
		self.rng = libtcod.random_get_instance()

	def generate_actions(self):
		events = []

		for entity in filter(lambda ent: ent.get_attribute(AttributeTag.HostileProgram), self.manager.entities):
			new_position = Vec2d(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			if new_position[0] != 0:
				new_position[1] = 0
			events.append(Action(ActionTag.ProgramMovement, {'target_id':entity.id, 'value':new_position}))

		return events
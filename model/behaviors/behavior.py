from model.attribute import AttributeTag

class Behavior(object):
	def __init__(self, manager):
		self.manager = manager

	def generate_actions(self):
		return []

	def handle_action(self, action):
		return []

def is_memory_of_parent(parent, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == parent.id:
		return True
	return False


from attribute import AttributeTag

def is_owned_memory(parent_id, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == parent_id:
		return True
	return False

def is_hostile_memory(parent_id, ent):
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] != parent_id:
		return True
	return False

# Does not actually check for world tiles yet because they don't exist, will add relevant code when I get to implementing them
"""
Takes a list of entities filtered to a single world position and the entity id of the entity checking.
Returns a bool indicating whether the tile is considered occupied already for the purposes of the entity with ID provided. Checks world tiles, for hostile programs, etc. etc.
"""
def entities_occupy_position(parent_id, entities):
	return len(filter(lambda ent: ent.get_attribute(AttributeTag.HostileProgram) != False or is_hostile_memory(parent_id, ent), entities)) != 0
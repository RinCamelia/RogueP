from attribute import AttributeTag
from world_tile import WorldTile

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

def is_program_main_segment(entity):
	return entity.get_attribute(AttributeTag.Player) != False or entity.get_attribute(AttributeTag.HostileProgram) != False or entity.get_attribute(AttributeTag.NeutralProgram) != False

"""
Takes a list of entities filtered to a single world position and the entity id of the entity checking.
Returns a bool indicating whether the tile is considered occupied already for the purposes of the entity with ID provided. Checks world tiles, for hostile programs, etc. etc.
"""
def entities_occupy_position(parent_id, position_world_data):
	if position_world_data['tile'] != WorldTile.Empty:
		return True
	return len(filter(lambda ent: is_program_main_segment(ent) != False or is_hostile_memory(parent_id, ent), position_world_data['entities'])) != 0
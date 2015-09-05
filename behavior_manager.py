import libtcodpy as libtcod
import objects.behavior, objects.event, objects.entity, objects.attribute
from objects.attribute import AttributeTag

class EntityManager:
	def __init__(self):
		self.behaviors = set()
		self.entities = []
		self.newest_entity_id = 0
		#arguably bad but i don't want to go digging in introspection just yet to figure out how to make this automatic
		self.behaviors.add(objects.behavior.PlayerMovementBehavior(self))

	def get_new_entity_id(self):
		self.newest_entity_id += 1
		return self.newest_entity_id

	def add_entity(self, entity):
		entity.id = self.get_new_entity_id()
		self.entities.append(entity)

	def get_entity_by_id(self, id):
		filtered = filter(lambda ent: ent.id == id, self.entities)
		if filtered != []:
			return filtered[0]
		raise IndexError( 'attempted to get nonexistent entity with ID ' + str(id))

	def remove_entity_by_id(self, id):
		self.entities = filter(lambda ent: ent.id != id, self.entities)	

	def handle_event(self, event):

		for beh in self.behaviors:
			beh.handle_event(event)

	def update_behaviors(self, delta):
		for beh in self.behaviors:
			for entity in self.entities:
				beh.apply_to_entity(entity)
			beh.apply_to_all_entities()
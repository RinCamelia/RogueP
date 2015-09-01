import objects.behavior, objects.event, objects.entity, objects.attribute

class BehaviorManager:
	def __init__(self):
		self.behaviors = set()
		#arguably bad but i don't want to go digging in introspection just yet to figure out how to make this automatic
		self.behaviors.add(objects.behavior.DrawBehavior(self))
		self.behaviors.add(objects.behavior.PlayerMovementBehavior(self))

	def handle_event(self, event, entities):
		for beh in self.behaviors:
			beh.handle_event(event, entities)

	def update_behaviors(self, entities):
		self.entities = entities
		for beh in self.behaviors:
			for entity in self.entities:
				beh.apply_to_entity(entity)
			beh.apply_to_all_entities(self.entities)
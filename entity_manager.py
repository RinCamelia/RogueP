import libtcodpy as libtcod
from model.behavior import PlayerMovementBehavior
from ui.ui_event import UIEvent, UIEventType

#Entity manager does two things right now: 1. manages game state entities (including ID assignment, fetching by ID, and )
#I just moved that code here and thinking back on it, it may not have been strictly necessary, but it makes keeping the internal details of actually mutating model state in one spot
#Or perhaps I just need to rename this again to ModelManger or something, the alternative is moving open a lot more behavior management functionality to MenuGame
class EntityManager:
	def __init__(self, parent_menu):
		self.behaviors = self.get_behaviors()
		self.entities = []
		self.newest_entity_id = 0

		self.parent_menu = parent_menu

		self.update_timer = 0
		self.update_delay = 500
		self.queued_actions = []
		self.is_executing = False

	#walk the subclass tree for Behavior and instantiate a copy of all of its most-derived subclasses
	def get_behaviors(self):
		results = []
		results.append(PlayerMovementBehavior(self))
		return results

	def queue_action(self, action):
		self.queued_actions.append(action)

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
		raise IndexError('attempted to get nonexistent entity with ID ' + str(id))

	def remove_entity_by_id(self, id):
		self.entities = filter(lambda ent: ent.id != id, self.entities)	

	def handle_action(self, action):
		action_results = []
		for beh in self.behaviors:
			behavior_action_results = beh.handle_action(action)
			if behavior_action_results:
				action_results.extend(behavior_action_results)

		return action_results

	def start_execution(self):
		if len(self.queued_actions) > 0:
			self.queued_actions.reverse()
			self.is_executing = True

	def process_single_queued_action(self, action):
		resulting_actions = self.handle_action(action)

		while len(resulting_actions) > 0:
			temp_action_list = []
			for resulting_action in resulting_actions:
				individual_action_results = self.handle_action(resulting_action)
				temp_action_list.extend(individual_action_results)
			resulting_actions = temp_action_list

	def update(self, delta):

		if self.is_executing and len(self.queued_actions) > 0:
			self.update_timer += delta

			if self.update_timer >= self.update_delay:
				self.update_timer = 0
				current_action = self.queued_actions.pop()
				self.process_single_queued_action(current_action)
				#this is the only line of code that depends on the outside world to any degree. I *REALLY* don't like doing this, and may consider a callback model in the future 
				#for now it is the simple way to tell the UI that we processed an action without doing nasty voodoo in MenuGame
				self.parent_menu.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueRemove, {'action': current_action}))
				if len(self.queued_actions) == 0:
					self.is_executing = False

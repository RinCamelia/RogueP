import libtcodpy as libtcod
from model.behavior import PlayerMovementBehavior
from ui.ui_event import UIEvent, UIEventType

###############################
###############################
# TODO: Rewrite initialization to scrape and produce a list of behaviors that are the most derived subclasses, for the purposes of calling behavior execution on them
# then its as simple as building validation and such through subclassing
# next challenge: handle behavior targeting



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

		#the only issue i can think of with this is if an action gets generated and queued and is then later invalidated by an action already in the current set of processing commands
		#cases like generating a move order into a tile that is now blocked, dealing damage to a target that is killed, trying to execute a library on a memory section that is now out of range, etc.
		#which really to me says i need good validation logic, not that the batching is a bad idea

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
				self.parent_menu.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueRemove, {'action': current_action}))
				if len(self.queued_actions) == 0:
					self.is_executing = False

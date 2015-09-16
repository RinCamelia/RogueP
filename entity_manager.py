import libtcodpy as libtcod
from ui.ui_event import UIEvent, UIEventType
from model.behaviors.behavior_program_movement import ProgramMovementBehavior
from model.behaviors.behavior_program_memory import ProgramMemoryAddBehavior, ProgramMemoryRemoveBehavior
from model.behaviors.behavior_ai_randomwalk import AIRandomWalkBehavior
from model.behaviors.behavior_damage_position import DamagePositionBehavior
from model.attribute import AttributeTag
from model.world_tile import WorldTile

#Entity manager does two things right now: 1. manages game state entities (including ID assignment, fetching by ID and position, and removing by id) and 2: input queue processing when told to by MenuGame
#I just moved that code here and thinking back on it, it may not have been strictly necessary, but it makes keeping the internal details of actually mutating model state in one spot
#Or perhaps I just need to rename this again to ModelManger or something, the alternative is moving a lot more behavior management functionality to MenuGame
class EntityManager:
	def __init__(self, parent_menu):
		self.behaviors = self.get_behaviors()
		self.entities = {}
		self.world_tiles = []
		self.newest_entity_id = 0

		self.parent_menu = parent_menu

		self.update_timer = 0
		self.update_delay = 250
		self.queued_actions = []
		self.action_history = []
		self.is_executing = False
		self.make_empty_world_temp()


	def make_empty_world_temp(self):
		for y in range(50):
			row = []
			for x in range(50):
				tile_type = WorldTile.Empty
				if x == 0 or x == 49 or y == 0 or y == 49:
					#make walls borders
					tile_type = WorldTile.Wall
				row.append({'tile': tile_type, 'entities':[]})
			self.world_tiles.append(row)


	#walk the subclass tree for Behavior and instantiate a copy of all of its most-derived subclasses
	def get_behaviors(self):
		results = []
		results.append(ProgramMemoryAddBehavior(self))
		results.append(ProgramMemoryRemoveBehavior(self))
		results.append(ProgramMovementBehavior(self))
		results.append(AIRandomWalkBehavior(self))
		results.append(DamagePositionBehavior(self))
		return results

	def queue_action(self, action):
		self.queued_actions.append(action)
		self.action_history.append(action)

	def load_action_history(self, history):
		for action in history:
			self.process_single_queued_action(action)

	def get_new_entity_id(self):
		self.newest_entity_id += 1
		return self.newest_entity_id

	def add_entity(self, entity):
		entity.id = self.get_new_entity_id()
		self.entities[entity.id] = entity
		position_attribute = entity.get_attribute(AttributeTag.WorldPosition)
		if position_attribute:
			position = position_attribute.data['value']
			self.world_tiles[position[0]][position[1]]['entities'].append(entity)

	def get_entity_by_id(self, id):
		if id in self.entities:
			return self.entities[id]
		raise IndexError('attempted to get entity with ID ' + str(id) + ', which is nonexistent')

	def get_world_data_for_position(self, position):
		return self.world_tiles[position[0]][position[1]]


	def remove_entity_by_id(self, id):
		entity = self.entities[id]
		del self.entities[id]
		position_attribute = entity.get_attribute(AttributeTag.WorldPosition)
		if position_attribute:
			position = position_attribute.data['value']
			self.world_tiles[position[0]][position[1]]['entities'].remove(entity)


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
		for behavior in self.behaviors:
			resulting_actions.extend(behavior.generate_actions())
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
				pre_action_milli = libtcod.sys_elapsed_milli()

				self.update_timer = 0
				current_action = self.queued_actions.pop()
				self.process_single_queued_action(current_action)
				#this is the only line of code that depends on the outside world to any degree. I *REALLY* don't like doing this, and may consider a callback model in the future 
				#for now it is the simple way to tell the UI that we processed an action without doing nasty voodoo in MenuGame
				self.parent_menu.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueRemove, {'action': current_action}))
				if len(self.queued_actions) == 0:
					self.is_executing = False

				post_action_milli = libtcod.sys_elapsed_milli()
				print 'single action took ' + str(post_action_milli - pre_action_milli) + ' MS'
import libtcodpy as libtcod
import os
import pickle
from menu import Menu
from enum import Enum
from vec2d import Vec2d
from entity_manager import EntityManager

from menu_manager import MenuStatus

from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from model.action import Action, ActionTag


from ui.frame_manager import FrameManager
from ui.ui_event import UIEvent, UIEventType
from ui.frame_world import FrameWorld
from ui.frame_actions_overlay import FrameActionsOverlay
from ui.frame_action_clock import FrameActionClock

class GameState(Enum):
	Executing = 1
	TakingInput = 2

class MenuGame(Menu):

	def __init__(self, console_width, console_height):
		Menu.__init__(self, console_width, console_width)
		max_actions = 5
		#currently hardcoded to test player movement
		self.behavior_manager = EntityManager()
		self.frame_manager = FrameManager(self)
		world_frame = FrameWorld(console_width, console_height, self.behavior_manager)
		self.frame_manager.add_frame(world_frame)
		self.frame_manager.add_frame(FrameActionsOverlay(console_width, console_height, self.behavior_manager))
		self.frame_manager.add_frame(FrameActionClock(console_width, console_height, self.behavior_manager))
		saved_world_state = self.try_load_file()
		if saved_world_state:
			self.behavior_manager.entities = saved_world_state
		else:
			self.behavior_manager.add_entity(Entity([
						Attribute(AttributeTag.Player, {'max_actions_per_cycle': max_actions}),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.WorldPosition, {'value': Vec2d(20, 20)}),
						Attribute(AttributeTag.MaxProgramSize, {'value': 20}),
						Attribute(AttributeTag.DrawInfo, {'character': 64})
					])
				)


		self.queued_actions = []
		self.game_state = GameState.TakingInput
		self.flagged_exit = False
		#delay in ms between executing commands
		self.action_execute_delay = 250
		self.execute_timer = 0
		self.queued_action_count = 0

		# generate an initial set of UI events to set up the UI
		self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueMaxActionsChange, {'max_actions': max_actions}))

	def update(self, delta):
		#blind isinstance(thing, Action) doesn't work because Python looks for a relevant local variable, not to imports
		import model.action
		key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress

		if self.game_state == GameState.TakingInput:

			if key.vk != libtcod.KEY_CHAR and key.vk != libtcod.KEY_NONE:

				if key.vk in contextual_input_tree:

					if hasattr(contextual_input_tree[key.vk], ('__call__')):
						contextual_input_tree[key.vk](self)

					elif isinstance(contextual_input_tree[key.vk], model.action.Action):
						self.queue_action(contextual_input_tree[key.vk])

				elif key.vk in global_input_tree:

					if hasattr(global_input_tree[key.vk], ('__call__')):
						global_input_tree[key.vk](self)

					elif isinstance(global_input_tree[key.vk], model.action.Action):
						self.queue_action(global_input_tree[key.vk])
				# do nothing
			else:
				if chr(key.c) in contextual_input_tree:

					if hasattr(contextual_input_tree[chr(key.c)], ('__call__')):
						contextual_input_tree[chr(key.c)](self)

					elif isinstance(contextual_input_tree[chr(key.c)], Action):
						self.queue_action(contextual_input_tree[chr(key.c)])

				elif chr(key.c) in global_input_tree:

					if hasattr(global_input_tree[chr(key.c)], ('__call__')):
						global_input_tree[chr(key.c)](self)

					elif isinstance(global_input_tree[chr(key.c)], Action):
						self.queue_action(global_input_tree[chr(key.c)])

		elif self.game_state == GameState.Executing:
			if len(self.queued_actions) > 0:
				self.execute_timer += delta
				if self.execute_timer >= self.action_execute_delay:
					self.execute_timer = 0
					action = self.queued_actions.pop()
					print 'executing Action ' + str(action)
					self.behavior_manager.handle_action(action)
					self.queued_action_count -= 1
					self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueRemove, {'action': action}))
			else:
				print 'queue empty, ending execution'
				self.game_state = GameState.TakingInput
				self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueClear))

		if self.flagged_exit:
			return MenuStatus.Exit
			
		return MenuStatus.Okay

	def draw(self):
		self.frame_manager.draw()
		pass

	def try_load_file(self):
		if not os.path.isfile('world.sav'):
			return False
		save_file = open('world.sav', 'r')
		return pickle.load(save_file)

	def save_current_state(self):
		save_file = open('world.sav', 'w')
		pickle.dump(self.behavior_manager.entities, save_file)

	def flag_for_exit(self):
		self.flagged_exit = True

	def queue_action(self, action):
		player = filter(lambda ent: ent.get_attribute(AttributeTag.Player), self.behavior_manager.entities)[0]
		player_max_actions = player.get_attribute(AttributeTag.Player).data['max_actions_per_cycle']
		action_cost = action.data['cost']
		if self.queued_action_count + action_cost <= player_max_actions:
			self.queued_action_count += action_cost
			self.queued_actions.append(action)
			self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueAdd, {'action': action}))


	def execute_queued_actions(self):
		self.game_state = GameState.Executing
		# reverse the list; the commands are in sequential order, so the first one in the list is the first one to execute. This lets me treat the list as a stack and pop each command off
		self.queued_actions.reverse()
		self.execute_timer = 0
		print 'beginning queued commands execution'

	def clear_queued_actions(self):
		self.queued_actions = []
		self.queued_action_count = 0
		self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueClear))

global_input_tree = {
	'q': MenuGame.flag_for_exit,
	's': MenuGame.save_current_state
}

contextual_input_tree = {
	libtcod.KEY_UP: Action(ActionTag.PlayerMovement, {'value' : Vec2d(0, -1), 'cost':1}),
	libtcod.KEY_DOWN: Action(ActionTag.PlayerMovement, {'value' : Vec2d(0, 1), 'cost':1}),
	libtcod.KEY_LEFT: Action(ActionTag.PlayerMovement, {'value' : Vec2d(-1, 0), 'cost':1}),
	libtcod.KEY_RIGHT: Action(ActionTag.PlayerMovement, {'value' : Vec2d(1, 0), 'cost':1}),
	'e': MenuGame.execute_queued_actions,
	'a': MenuGame.clear_queued_actions
}
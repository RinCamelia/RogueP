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
from ui.frame_pseudo_terminal import FramePseudoTerminal

class GameState(Enum):
	Executing = 1
	TakingInput = 2
	Loading = 3


# Quasi-controller class
# This is loaded directly into the main execution stack in my game loop, takes input from the UI and converts it to actual game state mutation or other things like saving or quitting
# Also does very trivial state tracking of its own, right now only for whether it should be taking input and the gameplay side of player actions
# If you want to see world state and logic, go to the model folder
# If you want to see rendering and UI, go to the UI folder and look at the frame classes
# Raw input is handled in frame_pseudo_terminal in ui
class MenuGame(Menu):

	def __init__(self, console_width, console_height):
		Menu.__init__(self, console_width, console_width)

		max_actions = 10
		self.queued_actions_cost_so_far = 0
		self.action_history = []
		self.flagged_exit = False
		self.entity_manager = None
		self.game_state = GameState.TakingInput

		#try and load an action history. If that fails, try to load a save game state. 
		#If for either reason we didn't load a save game state, initialize a new entity manager and put in a player.
		loaded_action_history = self.try_load_action_history()
		if not loaded_action_history:
			self.entity_manager = self.try_load_savegame()

		if not self.entity_manager:
			#currently hardcoded to test player movement
			self.entity_manager = EntityManager(self)
			self.entity_manager.add_entity(Entity([
						Attribute(AttributeTag.Player, {'max_actions_per_cycle': max_actions}),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.WorldPosition, {'value': Vec2d(20, 20)}),
						Attribute(AttributeTag.MaxProgramSize, {'value': 5}),
						Attribute(AttributeTag.ClockRate, {'value': 2}),
						Attribute(AttributeTag.DrawInfo, {'character': 64, 'fore_color': libtcod.Color(255,0,255)})
					])
				)
			self.entity_manager.add_entity(Entity([
						Attribute(AttributeTag.HostileProgram),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.WorldPosition, {'value': Vec2d(40, 20)}),
						Attribute(AttributeTag.MaxProgramSize, {'value': 5}),
						Attribute(AttributeTag.ClockRate, {'value': 2}),
						Attribute(AttributeTag.DrawInfo, {'character': 121, 'fore_color': libtcod.Color(255,0,0)})
					])
				)

		self.frame_manager = FrameManager(self)

		world_frame = FrameWorld(console_width, console_height, self.frame_manager)
		self.frame_manager.add_frame(world_frame)
		self.frame_manager.add_frame(FrameActionsOverlay(console_width, console_height, self.frame_manager))

		action_clock = FrameActionClock(console_width, console_height, self.frame_manager)
		self.frame_manager.add_frame(action_clock)
		self.frame_manager.add_frame(FramePseudoTerminal(console_width, console_height, action_clock.width, console_height - action_clock.height, self.frame_manager))


		# generate an initial set of UI events to set up the UI
		self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueMaxActionsChange, {'max_actions': max_actions}))

	def update(self, delta):
		self.frame_manager.update(delta)
		self.entity_manager.update(delta)

		if self.game_state == GameState.Executing:
			if not self.entity_manager.is_executing:

				self.frame_manager.handle_ui_event(UIEvent(UIEventType.InputEnabled))
				self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueClear))

				self.game_state = GameState.TakingInput
				self.queued_actions_cost_so_far = 0

		#future possible optimization/redesign: batch out commands to no longer than x MS per tick to allow UI update of a loading screen
		elif self.game_state == GameState.Loading:
			for action in self.action_history:
				self.entity_manager.handle_action(action) # may need to convert to dumping into entity manager's queue and calling a load action history method
			self.game_state = GameState.TakingInput


		if self.flagged_exit:
			return MenuStatus.Exit
			
		return MenuStatus.Okay

	def draw(self):
		self.frame_manager.draw()
		pass

	def handle_input_command(self, input_command):
		if self.game_state == GameState.TakingInput:

			if input_command in contextual_input_tree:

				if hasattr(contextual_input_tree[input_command], ('__call__')):
					contextual_input_tree[input_command](self)

				elif isinstance(contextual_input_tree[input_command], Action):
					self.queue_action(contextual_input_tree[input_command])

			elif input_command in global_input_tree:

				if hasattr(global_input_tree[input_command], ('__call__')):
					global_input_tree[input_command](self)

				elif isinstance(global_input_tree[input_command], Action):
					self.queue_action(global_input_tree[input_command])
			else:
				self.frame_manager.handle_ui_event(UIEvent(UIEventType.InvalidCommand, {'command': input_command}))

	def try_load_savegame(self):
		if not os.path.isfile('world.sav'):
			return False
		save_file = open('world.sav', 'r')
		return pickle.load(save_file)

	def try_load_action_history(self):
		if not os.path.isfile('action_history.sav'):
			return False

		save_file = open('action_history.sav', 'r')
		action_history = pickle.load(save_file)
		self.action_history = action_history
		self.game_state = GameState.Loading
		return True

	def save_current_state(self):
		save_file = open('world.sav', 'w')
		pickle.dump(self.entity_manager, save_file)

	def save_action_history(self):
		save_file = open('action_history.sav', 'w')
		pickle.dump(self.action_history, save_file)

	def flag_for_exit(self):
		self.flagged_exit = True

	def queue_action(self, action):
		player = filter(lambda ent: ent.get_attribute(AttributeTag.Player), self.entity_manager.entities)[0]
		player_max_actions = player.get_attribute(AttributeTag.Player).data['max_actions_per_cycle']
		action_cost = action.data['cost']
		if self.queued_actions_cost_so_far + action_cost <= player_max_actions:
			self.queued_actions_cost_so_far += action_cost
			#manually attach the player as the target_id for now - this will need to change when options other than movement are implemented
			action.data['target_id'] = player.id
			self.entity_manager.queue_action(action)
			self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueAdd, {'action': action}))


	def execute_queued_actions(self):
		self.game_state = GameState.Executing
		self.frame_manager.handle_ui_event(UIEvent(UIEventType.InputDisabled))
		self.entity_manager.start_execution()
		print 'beginning queued commands execution'

	def clear_queued_actions(self):
		self.entity_manager.queued_actions = []
		self.queued_actions_cost_so_far = 0
		self.frame_manager.handle_ui_event(UIEvent(UIEventType.ActionQueueClear))

	def dump_entities(self):
		for entity in self.entity_manager.entities:
			print entity

	def dump_entity_manager_state(self):
		print self.entity_manager.is_executing
		print self.entity_manager.update_timer


#currently pending refactoring into its own structure of some kind, whether that be a class or in-place somewhere above
global_input_tree = {
	'q': MenuGame.flag_for_exit,
	's': MenuGame.save_current_state,
	'd': MenuGame.dump_entities,
	'f': MenuGame.save_action_history,
	'g': MenuGame.dump_entity_manager_state
}

contextual_input_tree = {
	chr(30): Action(ActionTag.ProgramMovement, {'value' : Vec2d(0, -1), 'cost':1}),
	chr(31): Action(ActionTag.ProgramMovement, {'value' : Vec2d(0, 1), 'cost':1}),
	chr(17): Action(ActionTag.ProgramMovement, {'value' : Vec2d(-1, 0), 'cost':1}),
	chr(16): Action(ActionTag.ProgramMovement, {'value' : Vec2d(1, 0), 'cost':1}),
	'e': MenuGame.execute_queued_actions,
	'a': MenuGame.clear_queued_actions
}
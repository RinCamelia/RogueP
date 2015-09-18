import libtcodpy as libtcod
import os
import pickle
from menu import Menu
from enum import Enum
from vec2d import Vec2d
from model.entity_manager import EntityManager

from menu_manager import MenuStatus

from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from model.action import Action, ActionTag

from ui.frame_manager import FrameManager
from ui.ui_event import UIEvent, UIEventType
from ui.game.frame_world import FrameWorld, WorldRenderType
from ui.game.frame_actions_overlay import FrameActionsOverlay
from ui.game.frame_action_clock import FrameActionClock
from ui.game.frame_pseudo_terminal import FramePseudoTerminal
from ui.game.frame_libraries import FrameLibraries
from ui.game.frame_commands import FrameCommands

class GameState(Enum):
	Executing = 1
	TakingInput = 2
	Loading = 3

#dont like doing globals but until we break away from pure testing mode
max_actions = 10

# Quasi-controller class
# This is loaded directly into the main execution stack in my game loop, takes input from the UI and converts it to actual game state mutation or other things like saving or quitting
# Also does very trivial state tracking of its own, right now only for whether it should be taking input and the gameplay side of player actions
# If you want to see world state and logic, go to the model folder
# If you want to see rendering and UI, go to the UI folder and look at the frame classes
# Raw input is handled in frame_pseudo_terminal in ui
class MenuGame(Menu):

	def __init__(self, width, height):
		Menu.__init__(self, width, height)

		self.queued_actions_cost_so_far = 0
		self.action_history = []
		self.flagged_exit = False
		self.entity_manager = None
		self.game_state = GameState.TakingInput

		#try and load a save game. if that fails, initialize a baseline entity manager and try to feed in an action history. If both fail, the game simply ends up in a newgame state
		self.entity_manager = self.try_load_savegame()
		if not self.entity_manager:
			#currently hardcoded to test player movement
			self.entity_manager = EntityManager(self)
			self.entity_manager.add_entity(Entity([
						Attribute(AttributeTag.Player, {'max_actions_per_cycle': max_actions}),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.OwnedMemory, {'segments':[]}),
						Attribute(AttributeTag.WorldPosition, {'value': Vec2d(2, 2)}),
						Attribute(AttributeTag.MaxProgramSize, {'value': 5}),
						Attribute(AttributeTag.ClockRate, {'value': 2}),
						Attribute(AttributeTag.DrawInfo, {'character': 64, 'fore_color': libtcod.Color(157,205,255), 'back_color': libtcod.black, 'draw_type': WorldRenderType.Character, 'z_level': 2})
					])
				)
			#for x in range(10):
			self.entity_manager.add_entity(Entity([
							Attribute(AttributeTag.HostileProgram),
							Attribute(AttributeTag.Visible),
							Attribute(AttributeTag.OwnedMemory, {'segments':[]}),
							Attribute(AttributeTag.WorldPosition, {'value': Vec2d(20, 10)}),  #libtcod.random_get_int(0, 5, 45), libtcod.random_get_int(0, 5, 45))}),
							Attribute(AttributeTag.MaxProgramSize, {'value': 5}),
							Attribute(AttributeTag.ClockRate, {'value': 2}),
							Attribute(AttributeTag.DrawInfo, {'character': 121, 'fore_color': libtcod.Color(255,0,0), 'back_color': libtcod.black, 'draw_type': WorldRenderType.Character, 'z_level': 2})
						])
					)

			self.try_load_action_history()
		else:
			self.entity_manager.parent_menu = self

		self.entity_manager.player_id = 1

		self.init_ui()

	def init_ui(self):
		self.frame_manager = FrameManager(self)

		libraries = FrameLibraries(self.width, self.height, self.frame_manager)
		action_clock = FrameActionClock(self.width, self.height, libraries.height, self.frame_manager)
		commands = FrameCommands(self.width, self.height, libraries.width, action_clock.height + libraries.height, self.frame_manager)

		terminal = FramePseudoTerminal(self.width, self.height, action_clock.width, self.height - action_clock.height - libraries.height, self.frame_manager)
		world_screen_position = Vec2d(action_clock.width, action_clock.height + libraries.height)
		world_frame = FrameWorld(self.width, self.height, world_screen_position[0], world_screen_position[1], self.frame_manager)
		world_overlay = FrameActionsOverlay(self.width, self.height, world_screen_position[0], world_screen_position[1], self.frame_manager)


		self.frame_manager.add_frame(libraries)
		self.frame_manager.add_frame(world_frame)
		self.frame_manager.add_frame(world_overlay)
		self.frame_manager.add_frame(action_clock)
		self.frame_manager.add_frame(commands)
		self.frame_manager.add_frame(terminal)

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
		reloaded_manager = open('world.sav', 'r')
		return pickle.load(reloaded_manager)

	def try_load_action_history(self):
		if not os.path.isfile('action_history.sav'):
			return False

		save_file = open('action_history.sav', 'r')
		action_history = pickle.load(save_file)
		self.entity_manager.load_action_history(action_history)
		self.game_state = GameState.Loading
		return True

	def save_current_state(self):
		save_file = open('world.sav', 'w')
		#remove back-reference, otherwise Bad Things Happen(TM)
		self.entity_manager.parent_menu = None
		pickle.dump(self.entity_manager, save_file)
		self.entity_manager.parent_menu = self

	def save_action_history(self):
		save_file = open('action_history.sav', 'w')
		pickle.dump(self.entity_manager.action_history, save_file)

	def flag_for_exit(self):
		self.flagged_exit = True

	def queue_action(self, action):
		player = self.entity_manager.get_entity_by_id(self.entity_manager.player_id)
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

	def snapshot_performance(self):
		self.frame_manager.should_measure = True


#currently pending refactoring into its own structure of some kind, whether that be a class or in-place somewhere above
global_input_tree = {
	'exit': MenuGame.flag_for_exit,
	'quit': MenuGame.flag_for_exit,
	'o': MenuGame.save_current_state,
	'p': MenuGame.save_action_history,
	'f': MenuGame.dump_entities,
	'g': MenuGame.dump_entity_manager_state,
	'h': MenuGame.snapshot_performance
}

contextual_input_tree = {
	chr(24): Action(ActionTag.ProgramMovement, {'value' : Vec2d(0, -1), 'cost':1}),
	chr(25): Action(ActionTag.ProgramMovement, {'value' : Vec2d(0, 1), 'cost':1}),
	chr(26): Action(ActionTag.ProgramMovement, {'value' : Vec2d(1, 0), 'cost':1}),
	chr(27): Action(ActionTag.ProgramMovement, {'value' : Vec2d(-1, 0), 'cost':1}),
	#temporary, will need to be improved by removing hardocded player id etc.
	'w': Action(ActionTag.DamagePosition, {'relative' : Vec2d(0, -1), 'attacker_id':1, 'cost': 2}),
	's': Action(ActionTag.DamagePosition, {'relative' : Vec2d(0, 1), 'attacker_id':1, 'cost': 2}),
	'd': Action(ActionTag.DamagePosition, {'relative' : Vec2d(1, 0), 'attacker_id':1, 'cost': 2}),
	'a': Action(ActionTag.DamagePosition, {'relative' : Vec2d(-1, 0), 'attacker_id':1, 'cost': 2}),
	'e': MenuGame.execute_queued_actions,
	'q': MenuGame.clear_queued_actions
}
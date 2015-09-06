import libtcodpy as libtcod
from menu import Menu
from menu_manager import MenuStatus
from behavior_manager import EntityManager
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from frame_action_clock import FrameActionClock
from objects.action import Action, ActionTag
from frame_manager import FrameManager
from frame_world import FrameWorld
from vec2d import Vec2d
from enum import Enum

class GameState(Enum):
	Executing = 1
	TakingInput = 2

class MenuGame(Menu):

	def __init__(self, console_width, console_height):
		Menu.__init__(self, console_width, console_width)
		#currently hardcoded to test player movement
		self.behavior_manager = EntityManager()
		self.frame_manager = FrameManager(self)
		world_frame = FrameWorld(console_width, console_height, self.behavior_manager)
		self.frame_manager.add_frame(world_frame)
		self.frame_manager.add_frame(FrameActionClock(console_width, console_height, self.behavior_manager))
		self.behavior_manager.add_entity(Entity([
					Attribute(AttributeTag.Player, {'max_actions_per_cycle': 5}),
					Attribute(AttributeTag.Visible),
					Attribute(AttributeTag.WorldPosition, {'value': Vec2d(20, 20)}),
					Attribute(AttributeTag.MaxProgramSize, {'value': 20}),
					Attribute(AttributeTag.DrawInfo, {'character': 64, 'draw_func': FrameWorld.draw_entity_as_character})
				])
			)

		self.queued_actions = []
		self.game_state = GameState.TakingInput
		self.flagged_exit = False
		#delay in ms between executing commands
		self.action_execute_delay = 250
		self.execute_timer = 0
		self.queued_action_count = 0


	def flag_for_exit(self):
		self.flagged_exit = True

	def checked_command_wrapper(self, command):
		player = filter(lambda ent: ent.get_attribute(AttributeTag.Player), self.behavior_manager.entities)[0]
		player_max_actions = player.get_attribute(AttributeTag.Player).data['max_actions_per_cycle']
		if self.queued_action_count < player_max_actions:
			self.queued_action_count += 1
			command(self)


	def add_move_up(self):
		self.queued_actions.append(Action(ActionTag.PlayerMovement, {'value': Vec2d(0, -1)}))

	def add_move_down(self):
		self.queued_actions.append(Action(ActionTag.PlayerMovement, {'value': Vec2d(0, 1)}))

	def add_move_left(self):
		self.queued_actions.append(Action(ActionTag.PlayerMovement, {'value': Vec2d(-1, 0)}))

	def add_move_right(self):
		self.queued_actions.append(Action(ActionTag.PlayerMovement, {'value': Vec2d(1, 0)}))

	def execute_commands(self):
		self.game_state = GameState.Executing
		# reverse the list; the commands were stacked, so the first one in the list is the first one to execute. This lets me treat the list as a stack and pop each command off
		self.queued_actions.reverse()
		self.execute_timer = 0
		print 'beginning queued commands execution'

	def clear_commands(self):
		self.queued_actions = []

	def update(self, delta):
		key = libtcod.console_check_for_keypress(True) #libtcod.console_check_for_keypress

		if self.game_state == GameState.TakingInput:

			if key.vk != libtcod.KEY_CHAR:
				if key.vk in contextual_input_tree:
					contextual_input_tree[key.vk](self)
				elif key.vk in global_input_tree:
					global_input_tree[key.vk](self)
				# do nothing
			else:
				if chr(key.c) in contextual_input_tree:
					contextual_input_tree[chr(key.c)](self)
				elif chr(key.c) in global_input_tree:
					global_input_tree[chr(key.c)](self)
		elif self.game_state == GameState.Executing:
			if len(self.queued_actions) > 0:
				self.execute_timer += delta
				if self.execute_timer >= self.action_execute_delay:
					self.execute_timer = 0
					Action = self.queued_actions.pop()
					print 'executing Action ' + str(Action)
					self.behavior_manager.handle_action(Action)
					self.queued_action_count -= 1
			else:
				print 'queue empty, ending execution'
				self.game_state = GameState.TakingInput

		if self.flagged_exit:
			return MenuStatus.Exit
			
		return MenuStatus.Okay

	def draw(self):
		self.frame_manager.draw()
		pass

global_input_tree = {
	'q': MenuGame.flag_for_exit,
}

contextual_input_tree = {
	libtcod.KEY_UP: lambda self: self.checked_command_wrapper(MenuGame.add_move_up),
	libtcod.KEY_DOWN: lambda self: self.checked_command_wrapper(MenuGame.add_move_down),
	libtcod.KEY_LEFT: lambda self: self.checked_command_wrapper(MenuGame.add_move_left),
	libtcod.KEY_RIGHT: lambda self: self.checked_command_wrapper(MenuGame.add_move_right),
	'e': MenuGame.execute_commands,
	'a': MenuGame.clear_commands
}
import libtcodpy as libtcod
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from behavior_manager import BehaviorManager

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
limit_fps = 10
behavior_manager = BehaviorManager()
entities = []

entities.append(
	Entity([
			Attribute(AttributeTag.Player),
			Attribute(AttributeTag.Visible),
			Attribute(AttributeTag.WorldPosition, {'x': 20, 'y': 20}),
			Attribute(AttributeTag.CharacterDrawInfo, {'character': '@'})
		])
	)


libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'RogueP pre-dev', False)
libtcod.sys_set_fps(limit_fps)

def handle_keys():
	global playerx, playery
	key = libtcod.console_check_for_keypress()
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
	elif key.vk == libtcod.KEY_ESCAPE:
		return True  #exit game

while not libtcod.console_is_window_closed():

	behavior_manager.update_behaviors(entities)

	exit = handle_keys()
	if exit:
		break
import libtcodpy as libtcod
import objects.entity
import objects.attribute
from objects.attribute import Attribute, AttributeTag
import objects.event
import objects.behavior
import behavior_manager

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
BEHAVIOR_MANAGER = behavior_manager.BehaviorManager()
ENTITIES = []

ENTITIES.append(
	objects.entity.Entity([
			Attribute(AttributeTag.Player),
			Attribute(AttributeTag.Visible),
			Attribute(AttributeTag.WorldPosition, {'x': 20, 'y': 20}),
			Attribute(AttributeTag.CharacterDrawInfo, {'character': '@'})
		])
	)


libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'RogueP pre-dev', False)

def handle_keys():
	global playerx, playery
	key = libtcod.console_check_for_keypress()
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
	elif key.vk == libtcod.KEY_ESCAPE:
		return True  #exit game

while not libtcod.console_is_window_closed():

	BEHAVIOR_MANAGER.update_behaviors(ENTITIES)

	exit = handle_keys()
	if exit:
		break
import libtcodpy as libtcod
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from behavior_manager import BehaviorManager
from ui.menu import Menu
from ui.menu_main import MenuMain
from ui.menu_manager import MenuManager


screen_width = 80
screen_height = 50
limit_fps = 20
menu_manager = MenuManager(MenuMain(screen_width, screen_height))

libtcod.console_disable_keyboard_repeat()

libtcod.console_set_custom_font('consolas12x12_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(screen_width, screen_height, 'RogueP pre-dev', False)
libtcod.sys_set_fps(limit_fps)

while not libtcod.console_is_window_closed():
	#behavior_manager.update_behaviors(entities)
	if not menu_manager.loop(0):
		break
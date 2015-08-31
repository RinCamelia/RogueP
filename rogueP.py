import libtcodpy as libtcod
from objects.attribute import Attribute, AttributeTag
from objects.entity import Entity
from behavior_manager import BehaviorManager

screen_width = 80
screen_height = 50
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
libtcod.console_init_root(screen_width, screen_height, 'RogueP pre-dev', False)
libtcod.sys_set_fps(limit_fps)

while not libtcod.console_is_window_closed():
	behavior_manager.update_behaviors(entities)
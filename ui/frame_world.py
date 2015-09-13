import libtcodpy as libtcod
from model.attribute import AttributeTag
from frame import Frame
from vec2d import Vec2d
from enum import Enum
from model.entity_utilities import *

class WorldRenderType:
	Character = 1
	Memory = 2

# Draws world state to the screen
# If you want input management, see frame_pseudo_terminal
# If you want input processing and initialization, see menu_game in logic
# if you want to see the world state objects and behaviors, see the model folder
class FrameWorld(Frame):

	def __init__(self, root_console_width, root_console_height, world_x_start, world_y_start, frame_manager):
		Frame.__init__(self, root_console_width, root_console_height, root_console_width - world_x_start, root_console_height - world_y_start, frame_manager)
		self.entity_manager = frame_manager.parent_menu.entity_manager
		self.world_x_start = world_x_start
		self.world_y_start = world_y_start

	def update(self, delta):
		# may need update logic, for now, nothing
		pass

	def draw(self):
		libtcod.console_clear(self.console)

		#handy thing about this is it should help farther down the line when I go to implement FOV
		render_data = []
		for entity in self.entity_manager.entities:
			if entity.get_attribute(AttributeTag.Visible):
				position_info = entity.get_attribute(AttributeTag.WorldPosition)
				if not position_info:
					raise LookupError('entity ' + str(entity) + ' is flagged as visible, but does not have any world position')
				draw_info = entity.get_attribute(AttributeTag.DrawInfo)			
				if not draw_info:
					raise LookupError('entity ' + str(entity) + ' is flagged as visible, but does not have any draw info')
				render_data.append({'draw_type': draw_info.data['draw_type'], 'z_level':draw_info.data['z_level'],'entity': entity})

		#z-sort the entities we're rendering so that things like world tiles can be drawn behind entities on those tiles
		render_data.sort(lambda data,other: cmp(data['z_level'], other['z_level']))


		for to_render in render_data:
			if to_render['draw_type'] in render_type_dict:
				render_type_dict[to_render['draw_type']](self, to_render['entity'])

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, self.world_x_start, self.world_y_start)

		#renders a ! at the topleftmost screen tile of where the world is set to render
		#uncomment if things break
		#libtcod.console_put_char_ex(0, self.world_x_start, self.world_y_start, ord('!'), libtcod.white, libtcod.black)

	def draw_as_character(self, entity):
		position_info = entity.get_attribute(AttributeTag.WorldPosition).data['value']
		draw_info = entity.get_attribute(AttributeTag.DrawInfo)
		if not draw_info:
			raise LookupError('entity ' + str(entity) + ' is flagged as visible, but does not have any drawing information')
		libtcod.console_put_char_ex(self.console, position_info.x, position_info.y, chr(draw_info.data['character']), draw_info.data['fore_color'], draw_info.data['back_color'])


	def draw_as_memory(self, entity):
		entity_position = entity.get_attribute(AttributeTag.WorldPosition).data['value']
		our_parent_id = entity.get_attribute(AttributeTag.ProgramMemory).data['parent_id']
		our_parent = self.entity_manager.get_entity_by_id(our_parent_id)

		adjacent_memory = self.get_adjacent_entities(entity, lambda ent: is_owned_memory(our_parent_id, ent) or ent.id == our_parent_id)
		render_character = self.get_connector_tile(adjacent_memory)

		our_parent_draw_info = our_parent.get_attribute(AttributeTag.DrawInfo)
		libtcod.console_put_char_ex(self.console, entity_position.x, entity_position.y, chr(render_character), our_parent_draw_info.data['fore_color'], our_parent_draw_info.data['back_color'])

	def get_adjacent_entities(self, entity, ent_filter=lambda ent: True):
		entity_position = entity.get_attribute(AttributeTag.WorldPosition).data['value']
		results = {
			'north': False,
			'south': False,
			'east': False,
			'west': False
		}

		for other in self.entity_manager.entities:
			other_position = other.get_attribute(AttributeTag.WorldPosition).data['value']
			if ent_filter(other):
				delta = entity_position - other_position
				if delta == Vec2d(0, -1):
					results['south'] = True
				elif delta == Vec2d(0, 1):
					results['north'] = True
				elif delta == Vec2d(-1, 0):
					results['east'] = True
				elif delta == Vec2d(1, 0):
					results['west'] = True
		return results

	def get_connector_tile(self, adjacent_entities):
		render_character = None
		# TODO: clean up this unholy abomination of ifs, possibly with an enum and one straight shot at calculating this info
		# please consult https://en.wikipedia.org/wiki/Code_page_437 for what these character codes are
		# Python requires an explicit flag to be set somewhere to allow use of special characters in source files 
		# and I haven't been able to figure out how to set it on a full project basis
		if (adjacent_entities['north'] or adjacent_entities['south']) and not (adjacent_entities['east'] or adjacent_entities['west']):
			render_character = 179
		elif (adjacent_entities['east'] or adjacent_entities['west']) and not (adjacent_entities['north'] or adjacent_entities['south']):
			render_character = 196

		elif (adjacent_entities['north'] and adjacent_entities['east']) and not (adjacent_entities['west'] or adjacent_entities['south']):
			render_character = 192
		elif (adjacent_entities['south'] and adjacent_entities['east']) and not (adjacent_entities['west'] or adjacent_entities['north']):
			render_character = 218
		elif (adjacent_entities['south'] and adjacent_entities['west']) and not (adjacent_entities['east'] or adjacent_entities['north']):
			render_character = 191
		elif (adjacent_entities['north'] and adjacent_entities['west']) and not (adjacent_entities['east'] or adjacent_entities['south']):
			render_character = 217
		elif (adjacent_entities['north'] and adjacent_entities['east'] and adjacent_entities['south']) and not (adjacent_entities['west']):
			render_character = 195
		elif (adjacent_entities['east'] and adjacent_entities['south'] and adjacent_entities['west']) and not (adjacent_entities['north']):
			render_character = 194
		elif (adjacent_entities['south'] and adjacent_entities['west'] and adjacent_entities['north']) and not (adjacent_entities['east']):
			render_character = 180
		elif (adjacent_entities['west'] and adjacent_entities['north'] and adjacent_entities['east']) and not (adjacent_entities['south']):
			render_character = 193
		else:
			render_character = 197

		return render_character
render_type_dict = {
	WorldRenderType.Character: FrameWorld.draw_as_character,
	WorldRenderType.Memory: FrameWorld.draw_as_memory,
}
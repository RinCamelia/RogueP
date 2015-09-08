import libtcodpy as libtcod
from model.attribute import AttributeTag
from frame import Frame
from vec2d import Vec2d

# UI drawing class for the actual game world, renders to the subset of the screen that is not UI
# or will, anyway, just draws right to the console atm
# right now scrapes game state directly to draw things - may (and probably will) in the future harvest UI events to update the UI (pulling info only when player scans, etc)
class FrameWorld(Frame):

	def __init__(self, root_console_width, root_console_height, frame_manager):
		Frame.__init__(self, root_console_width, root_console_height)
		self.entity_manager = frame_manager.parent_menu.entity_manager

	def update(self, delta):
		# may need update logic, for now, nothing
		pass

	def draw(self):
		clear_entities = []
		libtcod.console_clear(0)
		for entity in self.entity_manager.entities:
			if entity.get_attribute(AttributeTag.Visible):
				position_info = entity.get_attribute(AttributeTag.WorldPosition).data['value']
				if not position_info:
					raise LookupError('entity ' + str(entity) + ' is flagged as visible, but does not have any world position')
				if entity.get_attribute(AttributeTag.Player):
					self.draw_entity_as_character(entity)	
				elif entity.get_attribute(AttributeTag.ProgramMemory):
					self.draw_entity_as_memory(entity)

	def draw_entity_as_character(self, entity):
		position_info = entity.get_attribute(AttributeTag.WorldPosition).data['value']
		draw_info = entity.get_attribute(AttributeTag.DrawInfo)
		if not draw_info:
			raise LookupError('entity ' + str(entity) + ' is flagged as visible, but does not have any drawing information')
		libtcod.console_put_char(0, position_info.x, position_info.y, chr(draw_info.data['character']), libtcod.BKGND_NONE)

	def draw_entity_as_memory(self, entity):
		position_info = entity.get_attribute(AttributeTag.WorldPosition).data['value']
		has_north_connection = False
		has_south_connection = False
		has_east_connection = False
		has_west_connection = False
		render_character = 80
		entity_position = entity.get_attribute(AttributeTag.WorldPosition).data['value']

		our_parent_id = entity.get_attribute(AttributeTag.ProgramMemory).data['parent_id']
		our_parent = self.entity_manager.get_entity_by_id(our_parent_id)
		for other in self.entity_manager.entities:
			is_memory = other.get_attribute(AttributeTag.ProgramMemory)	
			if is_memory and is_memory.data['parent_id'] == our_parent_id:
				other_position = other.get_attribute(AttributeTag.WorldPosition).data['value']
				if entity_position.get_distance(other_position) == 1:
					delta = entity_position - other_position
					if delta == Vec2d(0, -1):
						has_south_connection = True
					elif delta == Vec2d(0, 1):
						has_north_connection = True
					elif delta == Vec2d(-1, 0):
						has_east_connection = True
					elif delta == Vec2d(1, 0):
						has_west_connection = True
		our_parent_delta = entity_position - (our_parent.get_attribute(AttributeTag.WorldPosition).data['value'])
		if our_parent_delta == Vec2d(0, -1):
			has_south_connection = True
		elif our_parent_delta == Vec2d(0, 1):
			has_north_connection = True
		elif our_parent_delta == Vec2d(-1, 0):
			has_east_connection = True
		elif our_parent_delta == Vec2d(1, 0):
			has_west_connection = True

		#TODO: clean up this unholy abomination of ifs, possibly with an enum and one straight shot at calculating this info
		# please consult https://en.wikipedia.org/wiki/Code_page_437 for what these character codes are
		if (has_north_connection or has_south_connection or has_north_connection and has_south_connection) and not (has_east_connection or has_west_connection):
			render_character = 179
		elif (has_west_connection or has_east_connection or has_west_connection and has_east_connection) and not (has_north_connection or has_south_connection):
			render_character = 196
		elif has_west_connection and has_north_connection and not (has_east_connection or has_south_connection):
			render_character = 217
		elif has_north_connection and has_east_connection and not (has_west_connection or has_south_connection):
			render_character = 192
		elif has_east_connection and has_south_connection and not (has_west_connection or has_north_connection):
			render_character = 218
		elif has_south_connection and has_west_connection and not (has_east_connection or has_north_connection):
			render_character = 191
		elif has_west_connection and has_north_connection and has_east_connection and not has_south_connection:
			render_character = 193
		elif has_north_connection and has_east_connection and has_south_connection and not has_west_connection:
			render_character = 195
		elif has_east_connection and has_south_connection and has_west_connection and not has_north_connection:
			render_character = 194
		elif has_south_connection and has_west_connection and has_north_connection and not has_east_connection:
			render_character = 180
		else:
			render_character = 197
		libtcod.console_put_char(0, position_info.x, position_info.y, chr(render_character), libtcod.BKGND_NONE)
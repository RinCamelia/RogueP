import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld

class Behavior(object):
	def __init__(self, manager):
		self.manager = manager

	def generate_actions(self):
		return []

	def handle_action(self, action):
		return []

def is_memory_of_parent(parent, ent): 
	is_memory = ent.get_attribute(AttributeTag.ProgramMemory)
	if is_memory != False and is_memory.data['parent_id'] == parent.id:
		return True
	return False


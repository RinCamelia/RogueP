from enum import Enum

class AttributeTag(Enum):
	Base = 1
	Player = 2
	WorldPosition = 3
	CharacterDrawInfo = 4
	Visible = 5

class Attribute:
	def __init__(self, tag=AttributeTag.Base,data={}):
		self.tag = tag
		self.data = data
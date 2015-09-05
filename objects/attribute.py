from enum import Enum

class AttributeTag(Enum):
	Base = 1
	Player = 2
	WorldPosition = 3
	CharacterDrawInfo = 4
	Visible = 5
	MaxProgramSize = 6,
	ProgramMemory = 7

class Attribute:
	def __str__(self):
		return str(self.tag) + str(self.data)

	def __init__(self, tag=AttributeTag.Base,data={}):
		self.tag = tag
		self.data = data
from enum import Enum

class AttributeTag(Enum):
	Empty = 1
	Player = 2
	HostileProgram = 3
	ProgramMemory = 4
	NeutralProgram = 5
	Visible = 6
	DrawInfo = 7
	WorldPosition = 8
	MaxProgramSize = 9
	ClockRate = 10
	WorldTile = 11

class Attribute:
	def __str__(self):
		return str(self.tag) + ' ' + str(self.data)

	def __init__(self, tag=AttributeTag.Empty,data={}):
		self.tag = tag
		self.data = data
from enum import Enum

class ActionTag(Enum):
	Base = 1
	ProgramMovement = 2
	ProgramMemoryAdd = 3
	ProgramMemoryRemove = 4

class Action:
	def __str__(self):
		return 'Action with type ' + str(self.type) + ' and additional data ' + str(self.data)

	def __init__(self, type=ActionTag.Base, data={}):
		self.data = data
		self.type = type
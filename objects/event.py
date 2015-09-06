from enum import Enum
class ActionTag(Enum):
	Base = 1
	PlayerMovement = 2

class Action:
	def __str__(self):
		return str(self.type)

	def __init__(self, type=ActionTag.Base, data={}):
		self.data = data
		self.type = type
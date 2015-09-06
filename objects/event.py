from enum import Enum
class EventTag(Enum):
	Base = 1
	PlayerMovement = 2

class Event:
	def __str__(self):
		return str(self.type)

	def __init__(self, type=EventTag.Base, data={}):
		self.data = data
		self.type = type
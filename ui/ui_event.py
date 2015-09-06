from enum import Enum

class UIEventType(Enum):
	Empty = 1
	ActionCountChange = 2

class UIEvent:
	def __str__(self):
		return str(self.type)

	def __init__(self, type=UIEventType.Empty, data={}):
		self.data = data
		self.type = type
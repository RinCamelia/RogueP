from enum import Enum

class UIEventType(Enum):
	Empty = 1
	ActionQueueAdd = 2
	ActionQueueRemove = 3
	ActionQueueClear = 4
	ActionQueueMaxActionsChange = 5

class UIEvent:
	def __str__(self):
		return str(self.type)

	def __init__(self, type=UIEventType.Empty, data={}):
		self.data = data
		self.type = type
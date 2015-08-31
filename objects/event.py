from enum import Enum
class EventTag(Enum):
	Base = 1

class Event:
	def __init__(self, type=EventTag.Base, args={}):
		self.args = args
		self.type = type
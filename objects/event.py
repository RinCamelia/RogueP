import behavior, entity, attribute, enum

EVENT_TYPES = enum.Enum(["Base"])

class Event:
	def __init__(self, type=EVENT_TYPES.Base, *args):
		self.args = args
		self.type = type
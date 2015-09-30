from action import ActionTag
from targeting_type import TargetingType

class Function:
	def __init__(self,name="MISSING", action_tag=ActionTag.Base, targeting_type=TargetingType.MouseCoords, cost=1):
		self.name = name
		self.action_tag = action_tag
		self.targeting_type = targeting_type
		self.cost = cost
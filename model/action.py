from enum import Enum

# basic idea:
# all data going into the model gets boxed in PlayerActionValidate actions, which gives a WorldClockBehavior a chance to verify that the action makes sense 
# (not walking into walls or other programs, etc.)
# This class will also handle generating additional actions to trigger AI movement
class ActionTag(Enum):
	Base = 1
	ProgramMovement = 2
	PlayerActionValidate = 3

class Action:
	def __str__(self):
		return 'Action with type ' + str(self.type) + ' and additional data ' + str(self.data)

	def __init__(self, type=ActionTag.Base, data={}):
		self.data = data
		self.type = type
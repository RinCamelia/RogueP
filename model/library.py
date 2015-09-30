from action import ActionTag
from targeting_type import TargetingType

#TODO: move to somewhere in config
max_functions_per_library = 4

class Library:
	def __init__(self, name="MISSING", description="MISSING", functions=[]):
		self.name = name
		self.description = description
		self.functions = functions

	def remove_function_by_name(self, name):
		self.functions = filter(lambda func: not func.name == name, self.functions)

	def add_function(self, func):
		if len(self.functions) < max_functions_per_library:
			self.functions.append(func)
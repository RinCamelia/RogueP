import attribute

class Entity:
	def __init__(self):
		self.attributes = []

	def add_attribute(self, attribute):
		self.attributes.append(attribute)

	def remove_attribute(self, attribute):
		self.attributes = self.attributes.filter(lambda attr: not attr.is_kind(attribute_type))

	def has_attribute(self, attribute_type):
		return self.attributes.filter(lambda attr: attr.is_kind(attribute_type))
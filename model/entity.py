from attribute import AttributeTag

class Entity:


	def __init__(self, attributes=[]):
		self.attributes = attributes

	def add_attribute(self, attribute):
		self.attributes.add(attribute)

	def remove_attribute(self, attribute_tag):
		self.attributes = filter(lambda attr: not attr.tag == attribute_tag, self.attributes)

	def get_attribute(self, attribute_tag):
		results = filter(lambda attr: attr.tag == attribute_tag, self.attributes)
		if results:
			return results[0]
		return False
class Addition(object):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return "+"

	def children(self):
		return [self.left, self.right]


class Multiplication(object):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def name(self):
		return "*"

	def children(self):
		return [self.left, self.right]


class Number(object):

	def __init__(self, value):
		self.value = value

	def name(self):
		return "num: " + str(self.value)

	def children(self):
		return []

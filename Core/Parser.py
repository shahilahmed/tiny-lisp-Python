from Core.Utils import *


class Parser:
	
	def __init__(self,tokens = []):
		self.tokens = copy.deepcopy(tokens)
		self.loc    = 0
	
	def is_eof(self):
		if self.loc < len(self.tokens):
			return False
		return True
		
	def token(self):
		return self.tokens[self.loc] if not self.is_eof() else None
		
	def next(self,offset = 1):
		if not self.is_eof():
			self.loc = self.loc + offset
		else:
			self.loc = None
			
	def match(self,value = ''):
		if self.is_eof() and self.token() == None:
			print("End of Input.")
			exit()
		if self.token() == value:
			self.next()
		else:
			print("Error in Parsing Excepted {} but got {}.".format(self.token(1),value))
			exit()

	def parse_atom(self):
		value = self.token()
		self.next()
		return value
		
	def parse_list(self):
		if self.token() == ')':
			print("parse_list: Excepted ( but got ).")
			exit()
		elif self.token() == '(':
			result = []
			self.match('(')
			while not self.is_eof() and self.token() != ')':
				result.append(self.parse_list())
			self.match(')')
			return result
		else:
			return self.parse_atom()

	def parse_lists(self):
		result = []
		while not self.is_eof() and self.token() == '(':
			result.append(self.parse_list())
		if self.token() == ')':
			print("parse_lists: Excepted ( but got ).")
			exit()
		return result
	
	def parse(self):
		result = self.parse_lists()
		return result


		
		


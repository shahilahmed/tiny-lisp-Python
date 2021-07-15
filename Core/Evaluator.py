from Core.Utils import *


class Environment():

	def __init__(self,inner = None,outer = None):
		self.inner = {} if inner == None else inner
		self.outer = outer
	
	def __str__(self):
		return "Environment: \n\ninner: {}\n\nouter: {}\n\n".format(self.inner,self.outer)
	
	def __repr__(self):
		return self.__str__()
	
	def exists(self,key = None):
		if key != None:
			if key in self.inner:
				return True
			if self.outer != None:
				return self.outer.exists(key)
			return False	
		return False
		
	def get_global(self):
		env = self
		while env != None:
			env = self.outer
		return outer
	
	def get(self,key = None):
		if self.exists(key):
			if key in self.inner:
				return self.inner[key]
			if self.outer != None:
				return self.outer.get(key)
		else:
			print("from get() {} doesnot exists.".format(key))
			exit()	
	
	def set(self,key = None,value = None):
		if True:
			if key in self.inner:
				if value != None:
					self.inner[key] = value
			if self.outer != None:
				return self.outer.set(key,value)
		else:
			print("from set() {} doesnot exists.".format(key))	
			exit()	
	
	def define(self,key = None,value = None):
		if not self.exists(key):
			if value != None:
				self.inner[key] = value
		else:
			print("from define() {} already defined.".format(key))		
			exit()
		
	
class Procedure(object):
	
	def __init__(self, params, body, env):
		self.params, self.body, self.env = params, body, env
	
	def __str__(self):
		return ''
		##return "params: {} \n\nbody: {} \n\nenv: {}".format(self.params,self.body,self.env)
	
	def __repr__(self):
		return self.__str__()
	
	def __call__(self,*args): 
		return evaluate_exp(self.body,Environment(dict(zip(self.params,args)),self.env))

def evaluate_arith(exp = [],env = {}):
	symbol = exp[0]
	result = evaluate_exp(exp[1],env)
	for arg in exp[2:]:
		if symbol == "add":
			result = result + evaluate_exp(arg,env)
		elif symbol == "sub":
			result = result - evaluate_exp(arg,env)
		elif symbol == "mul":
			result = result * evaluate_exp(arg,env)
		elif symbol == "div":
			result = result / evaluate_exp(arg,env)
		elif symbol == "mod":
			result = result % evaluate_exp(arg,env)
	return result

def evaluate_cond(exp = [],env = {}):
	symbol = exp[0]
	result = evaluate_exp(exp[1],env)
	for arg in exp[2:]:
		if symbol == "eq":
			result = result == evaluate_exp(arg,env)
		elif symbol == "ne":
			result = result != evaluate_exp(arg,env)
		elif symbol == "lt":
			result = result < evaluate_exp(arg,env)
		elif symbol == "le":
			result = result <= evaluate_exp(arg,env)
		elif symbol == "gt":
			result = result > evaluate_exp(arg,env)
		elif symbol == "ge":
			result = result >= evaluate_exp(arg,env)
	return result

def evaluate_bitwise(exp = [],env = {}):
	symbol = exp[0]
	result = evaluate_exp(exp[1],env)
	for arg in exp[2:]:
		if symbol == "and":
			result = result & evaluate_exp(arg,env)
		elif symbol == "or":
			result = result | evaluate_exp(arg,env)
		elif symbol == "not":
			result = ~(result | evaluate_exp(arg,env))
		elif symbol == "xor":
			result = result ^ evaluate_exp(arg,env)
		elif symbol == "shr":
			result = result >> evaluate_exp(arg,env)
		elif symbol == "shl":
			result = result << evaluate_exp(arg,env)
	return result


def evaluate_specials(exp = [],env = {}):
	symbol = exp[0]
	result = None
	if symbol == "lambda":
		result = Procedure(exp[1],exp[2],env)
	elif symbol == "defun":
		result = evaluate_exp(["define",exp[1][0],["lambda",exp[1][1:],exp[2]]],env)
	elif symbol == "define":
		if not env.exists(evaluate_exp(exp[1],env)):
			env.define(evaluate_exp(exp[1],env),evaluate_exp(exp[2],env))
		## result = evaluate_exp(exp[1],env)
	elif symbol == "set":
		env.set(exp[1],evaluate_exp(exp[2],env))
		## result = evaluate_exp(exp[1],env)
	elif symbol == "if":
		result = evaluate_exp(exp[2],env) if evaluate_exp(exp[1],env) else evaluate_exp(exp[3],env)
	elif symbol == "cond":
		for (p,e) in exp[1:]:
			if evaluate_exp(p,env): 
				result = evaluate_exp(e,env)
				break
	elif symbol == "block":
		for arg in exp[1:]:
			result = evaluate_exp(arg,env)
	return result

def evaluate_io(exp = [],env = {}):
	result = None
	symbol = exp[0]
	if symbol == "print":
		str_data = ""
		for arg in exp[1:]:
			res = evaluate_exp(arg,env)
			if res != None:
				str_data = str_data + "{}".format(str(res).strip("\""))
		print("{}".format(str_data),end="")
	elif symbol == "println":
		print()
	elif symbol == "input":
		result = int(input())
	return result

		
def	evaluate_exp(exp = [],env = {}):
	result = None
	if isinstance(exp,list):
		symbol = exp[0]
		if symbol in ["add","sub","mul","div","mod"]:
			result =  evaluate_arith(exp,env)
		elif symbol in ["eq","ne","lt","le","gt","ge"]:
			result =  evaluate_cond(exp,env)
		elif symbol in ["and","or","not","xor","shl","shr"]:
			result =  evaluate_bitwise(exp,env)
		elif symbol in ["lambda","if","defun","define","set","cond","block"]:
			result =  evaluate_specials(exp,env)
		elif symbol in ["print","println","input"]:
			result =  evaluate_io(exp,env)
		else:
			proc = evaluate_exp(symbol,env)
			if not callable(proc):
				print("{} is not a procedure.".format(proc))
				exit()
			if proc in [True,False]:
				return proc
			args = [evaluate_exp(arg,env) for arg in exp[1:]]
			result = proc(*args)
	elif isinstance(exp,str):
		if env.exists(exp):
			return env.get(exp)
		else:
			return exp
	elif isinstance(exp,int) or is_instance(exp,float):
		result = exp
	return result
	
def evaluate(tree = [],env = {}):
	tree = copy.deepcopy(tree)
	for exp in tree:
		result = evaluate_exp(exp,env)
	print()
	

	
	

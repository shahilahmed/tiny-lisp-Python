from Core.Utils import *


class Lexer:

	def is_digit(char = ''):
		return (char >= '0' and char <= '9')
	
	def is_identifier(char = ''):
		return (char.lower() >= 'a' and char.lower() <= 'z')
	
	@staticmethod
	def lex(source = ""):
		source = copy.deepcopy(source)
		source = source + '\n'
		result = []
		loc = 0
		while loc < len(source):
			if source[loc] in [' ','\n','\r','\t']:
				loc = loc + 1
			else:
				if source[loc] == "#":
					if source[loc] == "#":
						loc = loc + 1
						while loc < len(source):
							if source[loc] == "\n":
								break
							loc = loc + 1
					else:
						print("Invalid Comment -> Required # But got {}".format(source[loc + 1]))
						exit()
				elif source[loc] in ['(',')']:
					str_data = source[loc] 
					loc = loc + 1
					result.append(str_data)
				else:
					if Lexer.is_digit(source[loc]) or source[loc] == '.':
						str_data = ""
						while Lexer.is_digit(source[loc]) or source[loc] == '.':
							if not loc < len(source):
								break
							if str_data.count('.') > 1:
								print("Invalid Floating Point Number: {}".format(str_data))
								exit()
							str_data = str_data + source[loc]
							loc = loc + 1
						if str_data.count('.') == 1:
							result.append(float(str_data))
						else:
							result.append(int(str_data))
					elif Lexer.is_identifier(source[loc]) or source[loc] == '_':
						str_data = ""
						while Lexer.is_identifier(source[loc]) or  Lexer.is_digit(source[loc]) or source[loc] == '_':
							if not loc < len(source):
								break
							str_data = str_data + source[loc]
							loc = loc + 1
						symbols = {
							"TRUE"  : True,
							"FALSE" : False,
							"NIL"   : None
						}
						if str_data.upper() in symbols:
							result.append(symbols[str_data.upper()])
						else:	
							result.append(str_data)
					elif source[loc] == '"':
						loc = loc + 1
						str_data = ""
						while source[loc] != '"':
							if not loc < len(source):
								break
							if source[loc] == '\n':
								break
							if source[loc] == '\\':
								loc = loc + 1
								if source[loc] in ['n','t','t','b','a']:
									str_data = str_data + '\\' + source[loc]
								elif source[loc] in ['"']:
									str_data = str_data + source[loc]
								loc = loc + 1
							else:
								str_data = str_data + source[loc]
								loc = loc + 1
						if source[loc] == '"':
							loc = loc + 1
							str_data = "\"{}\"".format(str_data)
							result.append(str_data)
						else:
							print("Unterminated String: {}".format(str_data))
							exit()
					else:
						print("Invalid Character: {}".format(source[loc]))
						exit()
		return result


		
		
		

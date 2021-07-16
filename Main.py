from Core.Lexer  import *
from Core.Parser import *
from Core.Evaluator import *
from Core.Transpiler import *
from datetime import datetime

NAME    = "Tiny Lisp Python with Transpiler to Python"
VERSION = "v0.7.0"
AUTHOR  = "Md Shahil Ahmed"

env = Environment()
env.define("pi",3.14)

def transpile_source(source = ""):
	if len(source) != 0:
		tokens = Lexer.lex(source)
		tree   = Parser(tokens).parse()
		code   = transpile(tree)
		return code

def interpret_source(source = ""):
	if len(source) != 0:
		tokens = Lexer.lex(source)
		tree   = Parser(tokens).parse()
		evaluate(tree,env)

def interpret_file(path = ""):
	if file_exists(file_path_full(path)):
		interpret_source(file_get_contents(file_path_full(path)))

def transpile_file(path = ""):
	if file_exists(file_path_full(path)):
		filename = path.split("\\")[-1].split(".")[0]
		code = transpile_source(file_get_contents(file_path_full(path)))
		file_put_contents(filename + ".py",code)
		print("Path: {} has been transpiled to {} successfully.".format(path,filename + ".py"))

def interpret_repl(prompt = "tl>"):
	source  = ""
	history = []
	while True:
		try:
			source = source + input(prompt if len(source) == 0 else "... ")
			if source in ["exit","quit","bye"]:
				break
			if source.count('(') != source.count(')'):
				source = source + ' \n'
			else:
				source = source.replace('\n',' ')
				history.append(source)
				tokens = Lexer.lex(source)
				tree   = Parser(tokens).parse()
				result = evaluate_exp(tree[0],env)
				if result != None:
					print(result)
				source = ""
		except Exception as e:
			source = ""
			print(e)
		print()
	contents = "\n".join(history)
	contents  = ";;Session : {}\n{}\n\n".format(datetime.now(),contents)
	path = file_path_full("repl\session.tl")
	if file_exists(path):
		file_put_contents(path,file_get_contents(path) + contents)		
	else:
		file_put_contents(path,contents)		

def print_info():
	print()
	print("{} {} {}".format(NAME,VERSION,AUTHOR))
	print("Copyright {}".format(datetime.now().year))
	print()
	print("usage: python main.py")
	print()

def main():
	print_info()
	argv = sys.argv[1:]
	if len(argv) >= 1:
		command = argv.pop(0)
		argv = list(filter(lambda x : file_exists(file_path_full(x)),argv))
		if command == "-help":	
			print()
			print("python main.py -X path\\file_1.ext path\\file_2.ext path\\file_n.ext")
			print()
			print("Here -X is given below")
			print()
			print(" -h : help")
			print(" -r : to open REPL(Read-Evaluate-Print-Loop)")
			print(" -i : interpret one by one file(s)")
			print(" -l : link all file(s) and then interpret")
			print(" -t : transpile one by one file(s) to (*.py)")
			print()
		if command == "-r":	
			interpret_repl()
		elif command == "-i":	
			for path in argv:
				env = Environment()
				env.define("pi",3.14)
				interpret_file(path)
		elif command == "-l":	
			source = ""
			for path in argv:
				source = source + "{}\n".format(file_get_contents(file_path_full(path)))
			interpret_source(source)
		elif command == "-t":
			for path in argv:
				transpile_file(path)
		else:
			print("usage: python main.py -help")
	else:
		print("usage: python main.py -help")
	
if __name__ == "__main__":
	interpret_file("lib\\lib.tl")
	main()



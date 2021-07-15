import copy
import sys
import os
import re


def sanitize(str_data):
	str_data = str_data + '\n'
	str_data = re.sub(re.compile(";.*" ) ,"" ,str_data)
	str_data = str_data.strip()
	str_data = " ".join(str_data.split())
	return str_data

def file_path_full(path = ''):
	if len(path) != 0:
		path = '{}\\{}'.format(os.getcwd(),path) # Absolute Path
		return path

def file_path(path = ''):
	if len(path) != 0:
		path = '{}'.format(path) # Relative Path
		return path

def file_exists(path = ''):
	if len(path) != 0:
		return os.path.exists(path)
	return False

def file_get_contents(path = ''):
	if len(path) != 0:
		f = open(path,'r')
		contents = f.read()
		f.close()
		return contents

def file_put_contents(path = '',contents = ''):
	if len(path) != 0 and contents != 0:
		f = open(path,'w')
		f.write(contents)
		f.close()

		
		

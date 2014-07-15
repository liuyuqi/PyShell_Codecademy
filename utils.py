# utils.py
# definition of shell classes.

builtin_cmd_list = ["cd", "exit", "history"]
username = ""
cwd = ""
lwd = ""
pathvar = ""
history_list = []

class Command (object):
	'''The class for command, 
	   each cmd takes an instance of this class'''
	def __init__(self, user_input):
		self.cmdline = user_input
		self.cmd_found = False

	def print_cmd(self):
		print(self.cmdline)

def get_real_dir(fakedir):
	'''get the real dir name given the form starting with . or /'''
	fullname = ""
	if fakedir[0:2] == "..":
		if len(fakedir) == 2:
			fullname = cut_leaf(cwd)
		else:
			fullname = cut_leaf(cwd) + fakedir[2:]
	elif fakedir[0] == ".":
		if len(fakedir) == 1:
			fullname = cwd
		else:
			fullname = cwd + fakedir[1:]
	else:
		fullname = cwd + "/" + fakedir
	if fullname == "":
		fullname = "/"
	return fullname

def cut_leaf(givendir):
	'''returns the parent dir of a given path'''
	leng = len(givendir)
	for c in givendir[::-1]:
		if c == '/' and leng != len(givendir):
			break
		leng -= 1
	return givendir[:leng-1]

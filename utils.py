# utils.py
# definition of shell classes.

builtin_cmd_list = ["exit", "history"]
username = ""
cwd = ""
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

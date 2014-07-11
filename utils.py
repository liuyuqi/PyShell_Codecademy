# utils.py
# definition of shell classes.

username = ""
machinename = ""
cwd = ""

class command (object):
	'''The class for command, 
	   each cmd takes an instance of this class'''
	def __init__(self, user_input):
		self.cmdline = user_input

	def print_cmd(self):
		print(self.cmdline)

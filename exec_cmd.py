# exec_cmd.py
# find corresponding out-source cmds from system and executes.

import os
import utils

def find_out_cmd(typein):
	'''Finds out-source cmds in the PATH directories 
	and executes if any is found'''
	words = typein.split(" ")
	firstword = words[0].strip()
	path_list = utils.pathvar.split(":")
	for path in path_list:
		filepath = path+"/"+firstword
		if os.access(filepath, os.X_OK & os.R_OK):
			utils.history_list[-1].cmd_found = True
			exec_out(words)
			return

def exec_out(words):
	'''executes the out-source cmd'''
	pid = os.fork()
	if pid < 0:
		print("Fork error!")
	elif pid == 0:
		os.execvp(words[0], words)
	else:
		os.waitpid(pid, 0)

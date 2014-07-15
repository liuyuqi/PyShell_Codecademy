# exec_cmd.py
# find corresponding out-source cmds from system and executes.

import os
import utils
import bg

def find_out_cmd(typein):
	'''Finds out-source cmds in the PATH directories 
	and executes if any is found'''
	words = typein.split(" ")
	background = bg.is_back(words)
	firstword = words[0].strip()
	path_list = utils.pathvar.split(":")
	for path in path_list:
		filepath = path+"/"+firstword
		if os.access(filepath, os.X_OK & os.R_OK):
			utils.history_list[-1].cmd_found = True
			exec_out(words, background)
			return

def exec_out(words, background):
	'''executes the out-source cmd'''
	wait_type = 0
	if background == True:
		wait_type = os.WNOHANG
		words = words[:len(words)-1]
	pid = os.fork()
	if pid < 0:
		print("Fork error!")
	elif pid == 0:
		os.execvp(words[0], words)
	else:
		if background == True:
			utils.bg_list.append(pid)
		os.waitpid(pid, wait_type)

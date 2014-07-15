# bg.py

import utils
import os

def is_back(words):
	'''judges whether a cmd contains demands for background execution'''
	if words[len(words) - 1].strip() == "&":
		return True
	else:
		return False

def check_background_jobs():
	'''check background jobs and returns to the user if any'''
	if len(utils.bg_list) == 0:
		print("No background jobs running.")
	for pid in utils.bg_list:
		while pid in utils.bg_list:
			try:
				os.kill(pid, 0)
			except OSError:
				print("Process [%d] had already terminated." % pid)
				utils.bg_list.remove(pid)
			else:
				os.waitpid(pid, 0)

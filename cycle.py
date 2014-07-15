# cycle.py

from init import *
import utils
import builtin
import exec_cmd
import sys

def shell_cycle():
	'''The execution cycle of the shell'''
	char_in = input(getprompt())
	char_in = char_in.strip()
	if char_in.strip() != "":
		hist_add(char_in)
		cmd_find(char_in)
	update_info()

def getprompt():
	outstring = "%s [%s]> " % (utils.username, utils.cwd)
	return outstring

def hist_add(typein):
	'''add the current typed-in cmd to history'''
	newrecord = utils.Command(typein)
	utils.history_list.append(newrecord)

def cmd_find(typein):
	'''find the command and execute if found'''
	words = typein.split(" ")
	firstword = words[0].strip()
	#finds whether cmd is builtin ones or out-source ones
	if firstword not in utils.builtin_cmd_list:
		exec_cmd.find_out_cmd(typein)
	else:
		builtin.exec_builtin(typein)
	#cmd not found
	if utils.history_list[-1].cmd_found == False:
		print("Yuqish: command %s not found!\n" % typein)

def update_info():
	'''update information such as environment variables, etc...'''
	utils.username = os.getlogin()
	utils.cwd = os.getcwd()
	utils.pathvar = os.getenv('PATH')

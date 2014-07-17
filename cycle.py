# cycle.py

from init import *
import utils
import builtin
import exec_cmd
import bg
import sys

def shell_cycle():
	'''The execution cycle of the shell'''
	char_in = input(getprompt())
	typein = norm(char_in)
	if typein != "":
		hist_add(typein)
		cmd_find(typein)
	update_info()

def getprompt():
	outstring = "%s [%s]> " % (utils.username, utils.cwd)
	return outstring

def norm(char_in):
	'''eliminate all blanks'''
	words = char_in.split(" ")
	new_words = []
	idx = 0
	for word in words:
		while word in words and word.strip() == "":
			words.pop(idx)
		if word in words:
			new_words.append(word.strip())
		idx += 1
	#print(new_words)
	result = " ".join(new_words)
	return result

def hist_add(typein):
	'''add the current typed-in cmd to history'''
	newrecord = utils.Command(typein)
	utils.history_list.append(newrecord)

def cmd_find(typein):
	'''find the command and execute if found'''
	words = typein.split(" ")
	firstword = words[0].strip()
	#analyse grammar for redirection demands
	rd = bg.rd_analyse(words)
	#finds whether cmd is builtin ones or out-source ones
	if firstword not in utils.builtin_cmd_list:
		exec_cmd.find_out_cmd(typein, rd)
	else:
		builtin.exec_builtin(typein, rd)
	#cmd not found
	if utils.history_list[-1].cmd_found == False:
		print("Yuqish: command %s not found!\n" % typein)

def update_info():
	'''update information such as environment variables, etc...'''
	utils.username = os.getlogin()
	utils.cwd = os.getcwd()
	utils.pathvar = os.getenv('PATH')

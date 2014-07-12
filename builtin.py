# builtin.py
# functions of dealing with built-in commands

import utils

def exec_builtin(typein):
	'''find built-in cmds and executes it'''
	utils.history_list[-1].cmd_found = True
	words = typein.split(" ")
	firstword = words[0].strip()
	if firstword == "exit" or firstword == "quit":
		cmd_exit()
	if typein == "history":
		cmd_history()

def cmd_exit():
	'''quits the shell'''
	print("Thanks for using, bye!")
	print()
	exit()

def cmd_history():
	if utils.history_list == []:
		return
	num = 1
	for item in utils.history_list:
		print(str(num)+"  "+item.cmdline)
		num += 1

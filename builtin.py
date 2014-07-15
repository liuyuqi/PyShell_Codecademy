# builtin.py
# functions of dealing with built-in commands

import utils
import bg
import os

def exec_builtin(typein):
	'''find built-in cmds and executes it'''
	utils.history_list[-1].cmd_found = True
	words = typein.split(" ")
	firstword = words[0].strip()
	if firstword == "cd":
		cmd_cd(words)
	if firstword == "exit" or firstword == "quit":
		cmd_exit()
	if typein == "history":
		cmd_history()
	if typein == "fg":
		cmd_fg(words)

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

def cmd_cd(words):
	target_dir = ""
	if len(words) == 1:
		target_dir = os.getenv('HOME')
	else:
		secword = words[1]
		if secword == "-":
			if utils.lwd == "":
				print("cd: error: last dir doesn't exist!")
				return
			else:
				target_dir = utils.lwd
		else:
			target_dir = utils.get_real_dir(secword)

	os.chdir(target_dir)
	utils.lwd = utils.cwd

def cmd_fg(words):
	if len(words) != 1:
		print("Error: input must contain fg only.")
	bg.check_background_jobs()

# cycle.py

from init import *
import utils
import sys

def getprompt():
	outstring = "%s@[%s]> " % (utils.username, utils.cwd)
	return outstring

def shell_cycle():
	'''The execution cycle of the shell'''
	char_in = input(getprompt())
	char_in = char_in.strip()
	

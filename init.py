# init.py
import os
import socket
import utils

def sysinfo_init():
	'''init all states of system information'''
	
	#first get the current user name and machine hostname
	uname = os.getlogin()
	tmpchar = socket.gethostname()
	if tmpchar.find(".") is True:
		tmp = tmpchar.split(".")
		tmpchar = tmp[0]
	mname = tmpchar
	
	#then get the current working directory
	currwd = os.getcwd()
	
	#finally, init the global object 'sysinfo'
	utils.username = uname
	utils.machinename = mname
	utils.cwd = currwd

def shell_init():
	''' The initialization function for the shell'''
	print("Initializing shell... \n")
	sysinfo_init()
	print("Initialization finished! Welcome to use Yuqi Shell!")

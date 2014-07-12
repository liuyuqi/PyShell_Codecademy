# init.py
import os
import socket
import utils

def sysinfo_init():
	'''init all states of system information'''
	
	#first get the current user name and machine hostname
	utils.username = os.getlogin()
	
	#then get the current working directory
	utils.cwd = os.getcwd()
	
	#get the current PATH variable
	utils.pathvar = os.getenv('PATH')


def shell_init():
	''' The initialization function for the shell'''
	print("Initializing shell... \n")
	sysinfo_init()
	print("Initialization finished! Welcome to use Yuqi Shell!")

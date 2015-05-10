# bg.py

import utils
import os
import sys


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


def rd_analyse(words):
    '''analyse grammar for redirection demands'''
    result = rd_extract(words)
    if result != []:
        passed = rd_check(result, words)
    else:
        return None
    # print(result)
    if passed == False:
        return None
    else:
        return result


def rd_extract(words):
    '''Extract all redirection symbols from user input'''
    result = []
    index = 1
    for word in words[1:]:
        if "<" in word or ">" in word:
            if word.strip() == ">":
                result.append([index, 1, 'overwrite'])
            elif word.strip() == ">>":
                result.append([index, 1, 'append'])
            elif word.strip() == "2>":
                result.append([index, 2, 'overwrite'])
            elif word.strip() == "2>>":
                result.append([index, 2, 'append'])
            elif word.strip() == "&>":
                result.append([index, 3, 'overwrite'])
            elif word.strip() == "&>>":
                result.append([index, 3, 'append'])
            elif word.strip() == "<":
                result.append([index, 0, 'in'])
        index += 1
    return result


def rd_check(result, words):
    '''check whether redirection information is legal'''
    if len(result) > 2:
        print("Error: too many redirection demands!")
        return False
    elif len(result) == 2:
        if result[1][0] == len(words) - 1:
            print("Error: please check your input after the last redirection symbol.")
            return False
        if result[1][0] - result[0][0] != 2:
            print("Error: please check your input between the redirection symbols.")
            return False
        else:
            if result[0][1] != 0 and result[1][1] == 0:
                print("Error: format: command < file_in > file_out")
                return False
            elif result[0][1] == 0 and result[1][1] == 0:
                print("Error: cannot specify more than one input files!")
                return False
            elif result[0][1] > 0 and result[1][1] > 0:
                print("Error: cannot specify more than one output files!")
                return False
    elif len(result) == 1:
        if result[0][0] == len(words) - 1:
            print("Error: please check your input after the last redirection symbol.")
            return False
    return True


def start_rd_builtin(typein, rd):
    '''start the redirection of builtin cmds by changing
	file descriptors.'''
    if rd[0][1] == 0:
        print("Error: built-in commands doesn't support redirection of std input!")
        return [False, typein]
    words = typein.split(" ")

    # get the command without rd descriptions.
    typein = rd_eliminate(typein, rd)

    #get the target of redirection
    fake_target = words[rd[0][0] + 1]
    target = get_file_target(fake_target)

    #only one rd descriptor is permitted here, hense no loop is needed.
    fd = change_fd(target, rd[0])
    if fd == -1:
        return [False, typein]
    return [True, typein]


def start_rd(typein, rd):
    '''starts file redirection for out-source cmds,
	a little different from the start_rd_builtin() function'''
    if rd[0][1] == 0:
        print("Error: built-in commands doesn't support redirection of std input!")
        return typein
    words = typein.split(" ")

    # get the command without rd descriptions.
    typein = rd_eliminate(typein, rd)

    #get the target of redirection
    for item in rd:
        fake_target = words[item[0] + 1]
        target = get_file_target(fake_target)
        fd = change_fd_out(target, item)

    return typein


def stop_rd():
    '''Changes the file descriptors back to stdin/out/err'''
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    for fd in utils.history_list[-1].dirty_files:
        fd.close()


def change_fd_out(target, rd_member):
    '''changes the file descriptor, however the outsource version'''
    # First, determine the flags for file opening.
    aux = rd_get_flag_out(rd_member)

    #then, determine the file discriptor to replace.
    fd_to_replc = rd_get_orig_fd(rd_member)

    #finally, perform the file operation.
    try:
        fd = os.open(target, aux)
    except OSError:
        print("Error: cannot open file %s" % target)
        return -1
    else:
        for num in fd_to_replc:
            os.close(num)
            os.dup(fd)
            os.close(fd)
            utils.history_list[-1].dirty_files.append(fd)
        return fd


def change_fd(target, rd_member):
    '''changes the file descriptor as needed before redirection.
	NOTICE: this will only change ONE file descriptor'''

    # First, determine the flags for file opening.
    aux = rd_get_flag(rd_member)

    #then, determine the file discriptor to replace.
    fd_to_replc = rd_get_orig_fd(rd_member)

    #finally, perform the file operation.
    try:
        fd = open(target, aux)
    except OSError:
        print("Error: cannot open file %s" % target)
        return -1
    else:
        for num in fd_to_replc:
            if num == 0:
                sys.stdin = fd
            elif num == 1:
                sys.stdout = fd
            elif num == 2:
                sys.stderr = fd
            utils.history_list[-1].dirty_files.append(fd)
        return fd


def rd_get_flag(rd_member):
    '''Determine the flags for file opening.'''
    if rd_member[2] == "append":
        aux = "a"
    elif rd_member[2] == "overwrite":
        aux = "w+"
    elif rd_member[2] == "in":
        aux = "r"
    else:
        print("ERROR in program execution!")
        exit()
    return aux


def rd_get_flag_out(rd_member):
    '''Determine the flags for file opening. (the out-source version)'''
    if rd_member[2] == "append":
        aux = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    elif rd_member[2] == "overwrite":
        aux = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    elif rd_member[2] == "in":
        aux = os.O_RDONLY
    else:
        print("ERROR in program execution!")
        exit()
    return aux


def rd_get_orig_fd(rd_member):
    '''then, determine the file discriptor to replace.'''
    tmp = rd_member[1]
    if tmp == 0 or tmp == 1 or tmp == 2:
        fd_to_replc = [tmp]
    elif tmp == 3:
        fd_to_replc = [1, 2]
    else:
        print("ERROR in program execution!")
        exit()
    return fd_to_replc


def rd_eliminate(typein, rd):
    '''Eliminate the rd parts and return only the command itself'''
    words = typein.split(" ")
    index = rd[0][0]
    new_typein = " ".join(words[:index])
    return new_typein


def get_file_target(fake_target):
    '''This takes a fake file/directory target as input,
	and outputs the real target file/dir path'''
    if fake_target[0] != "/":
        target = utils.get_real_dir(fake_target)
    else:
        target = fake_target
    return target

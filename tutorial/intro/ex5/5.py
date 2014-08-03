# Loops

username = "user"
cwd = "/home"

# add the while loop at some point below. Notice the indentation!

prompt = "%s [%s]> " % (username, cwd)
user_input = raw_input(prompt)
args = user_input.split(" ")
print "This command is " + args[0]
print ""

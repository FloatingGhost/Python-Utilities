#CommandProcessor

##A service class to asyncronously process commands

###Usage

```python

from floatingutils.commandprocessor import *

#Arguments:

#delimeter (str): The delimeter for your function arguments

#command_prefix (str): What the processor expects to see at the
#front of commands, e.g. !help (prefix=!) or ~help (prefix ~)

#module_path (str): Optional, if you want to dynamically load functions
#into the processor, set this to the directory you keep your modules in

#admins (list): Optional, if you want admin-only commands, set this as
#the list of usernames you wish to use

#debug (bool): Optional, set the logging verbosity to debug


cmdproc = CommandProcessor(
              delimeter = ",",
              command_prefix = "!", 
              module_path    = "modules/",
          )

#Start the thread off
cmdproc.run()

#Set the callback for when a command completes
#This will just print any output
cmdproc.setCallback(print)

#Push a command 
cmdproc.push("!help")

#Define some functions for the processor to use
def myFunc():
  return 1

#Or with arguments, cmdproc supports auto-cast from type hints
def myFuncWithArguments(arg:int):
  return arg

#Add a function
#Arguments:
#Function_Name: The name by which to call the function
#Function_Object: The actual definition of the function
#cmdproc will automatically pull out the arguments/defaults/type hints :3
cmdproc.addCommand("myfunc", myFunc)
cmdproc.addCommand("myfuncargs", myFuncWithArguments)

#Run the newly added commands
cmdproc.push("!myfunc")
cmdproc.push("!myfuncargs 5")

#Get the output -- This will wait until there *is* output, so
#don't count on it exiting if your functions never return :<
#getOutput() gets the first output from the queue, so there may be a few
#things to get out of it
out = cmdproc.getOutput()
>>> out = "Help: blah blah blah memes"
out = cmdproc.getOutput()
>>> out = 1
out = cmdproc.getOutput()
>>> out = 5

#Stop the processor
#This will wait for the command queue to clear before exiting
cmdproc.exit()

#Force exit -- Will IMMEDIATELY exit
cmdproc.exit(True)

```

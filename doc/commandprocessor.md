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

#Get the output -- This will wait until there *is* output, so
#don't count on it exiting if your functions never return :<
out = cmdproc.getOutput()
>>>out = "Help: blah blah blah memes"

#Stop the processor
cmdproc.exit()

```

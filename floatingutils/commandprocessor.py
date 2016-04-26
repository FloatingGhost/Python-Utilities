#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'

import re
import argparse
import sys
import importlib
import traceback
from floatingutils.log import Log
import types

def listtostr(n):
  return ",".join(n)

class CommandProcessor:
  """A class to generically process commands, as defined by a list of commands and
     argparse parsers - used to extract arguments from a string"""

  def __init__(self, delimiter=",", prefix="!", modulePath=".", debug=False, admins=[]):
    self.log = Log()
    self.log.info("Command Processor Created, prefix {}".format(prefix))
    self.log.newline()
    self.log.info("CMDPROC INIT")
    self.log.line()
    self.log.incIndent()
    self.parsers = {}
    self.delimiter = delimiter
    self.functions = {}
    self.modules = []
    self.prefix = prefix
    ##Add the module path to PYTHONPATH
    sys.path.insert(0, modulePath)
    self.admins = admins
    if debug:
      self.log.setLevel(self.log.DEBUG)
    self._addConfigCommands()
    self.log.line()
    self.log.info("FINISHED CMDPROC INIT")   
    self.log.newline()

  def _addConfigCommands(self):
    """Add bot configuration commands"""
    self.log.info("Adding common commands...")
    self.log.incIndent()
    self.addCommand("help", "get help", "help", self.getHelp, ["program"])
    self.addCommand("quit", "quit", "quit", self.exit,need_admin=True)
    self.addCommand("import", "Import a module", "import [module]",
                    self.loadModule, ["mod"])
    self.addCommand("unload", "Unload a module", "unload [module]",
                    self.unloadModule, ["mod"])
    self.addCommand("reload", "Reload a module", "reload [module]", self.reloadModule,
                    ["mod"])
    self.addCommand("isadmin", "Check if a user is an admin", "isadmin [username]",
                    self.isAdmin, ["username"])
    self.addCommand("lsmod", "List currently loaded modules", "lsmod", self.lsmod)
    self.log.decIndent()
    self.log.info("Successfully added common commands.")

  def reloadModule(self, name):
    self.log.info("↻↻  Reloading {} ↻↻".format(name))
    yield "Reloading {}".format(name)
    self.log.incIndent()
    x = self.unloadModule(name)
    for i in x:
      yield i
    x = self.loadModule(name)
    for i in x:
      yield i
    self.log.decIndent()
    self.log.info("↻↻ Successfully reloaded {} ↻↻".format(name))
    yield "Reloaded {}".format(name)

  def lsmod(self):
    x = "Currently loaded modules:\n"
    y = "\n".join(self.modules)
    yield x+y

  def exit(self):
    """Shut the bot down"""
    
    yield ("Going to sleep.")
    sys.exit(1)

  def addCommand(self, name, description="", usage="", func=None, arglist=[], 
                 need_admin=False,module="Builtin"):
    """Add a command to our list
       arguments: 
          name: The name to call the function by, i.e !hello
          description: An extended description of what it does
          usage: A description of how to use the function
          func: A function object to call when we run it
          arglist: A list of argument names
          need_admin: Do we need elevated permissions to run it?
        returns:
          0 on Success
          1 on Failure """

    name = name.lower()
    if name[-1] == "_":
      self.log.warning("Not adding {}: Hidden function".format(name))
      return 0
    #If the user doesn't provide a function, we can't do anything
    if not func:
      self.log.warning("No function provided for {}.".format(name))
      return 1

    self.log.info("+ Adding cmd {}( {} )".format(name, ",".join(arglist)))
    ##Add an argument parser for the function
    parser = argparse.ArgumentParser(description=description, usage=usage)
    ##Add the parser to our list
    self.parsers[name] = parser
    
    self.functions[name] = self.Command(name,parser,func,arglist,module,need_admin)
    ##Add the arguments we want for this function
    for i in arglist:
      self.addArgument(name, i)
    return 1

  def removeCommand(self, name):
    """Remove a command from the list"""
    try:
      del self.functions[name]
    except:
      pass

  def loadModule(self, name):
    """Load an external module from module path"""
    print("LOADING {}".format(name))
    self.log.newline() 
    self.log.info("LOADING MODULE {}".format(name.upper())) 
    self.log.line()
    self.log.incIndent()
    try:
      ##Try loading the module as i
      self.log.debug("Importing {}...".format(name))
      i = importlib.import_module(name)
      ##In case it's changed and was imported before, reload it 
      self.log.debug("Reloading...")
      i = importlib.reload(i)
      ##Get a list of all the functions defined in the module
      self.log.debug("Getting functions...")
      funcs = dir(i)
      ##Don't import python's internal functions, like __name__ and __init__
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])

      self.log.debug("Loaded, adding functions...")
      self.log.incIndent()
      funcs = ""
      ##Load the functions in
      for j in z:
        self.log.debug("Adding function {}.{}".format(name,j))
        try:
          if j[-1] != "_":
            ##this will actually get the function object, not just its name
            k = eval(j)
            ##Get the variables used in the function
            args = k.__code__.co_varnames
            ##Get the number of arguments the function expects
            num = k.__code__.co_argcount
            defaults = k.__defaults__ or []
            numdefaults = len(defaults)
            ##Throw the function and arguments over to our addCommand
            l = j.split(".")[-1].lower() 
            funcs = "{}!{}{}, ".format(funcs, l,
                                      "(ADMIN)" if l[0] == "_" else "")
            self.addCommand(l, usage="{} {}".format(l, ", ".join(["["+x+"]" for x in args[:num-numdefaults]])), func=k, arglist=args[:num-numdefaults])
            self.log.debug("Successfully added function '{}'".format(l))
        except Exception as ex:
          ##In case it wasn't actually a function object
          pass
      self.log.decIndent()
      self.log.decIndent()
      self.log.line()
      self.log.info("LOADED {} SUCCESSFULLY".format(name.upper()))
      self.log.newline()
      yield "Inserted module {} ({})".format(name, funcs[:-2])
      self.modules.append(name)
      yield True
    except ImportError as ex:
      self.log.error("!!! Tried to import Non-existent module {}".format(name))
      self.log.error(ex)
      yield "Module {} does not exist".format(name)
    except Exception as e:
      self.log.error("!!! Failed with {} !!!".format(e))
      yield False
    
  def unloadModule(self, name):
    """Unload an entire external module"""
    self.log.info("-- Unloading module {} --".format(name))
    try:
      i = importlib.import_module(name)
      funcs = dir(i)      
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])
      for j in z: 
        self.log.debug("  Removing {}".format(j))        
        self.removeCommand(j.split(".")[-1])
      yield True  
      self.modules.remove(name)
      self.log.info("-- Successfully unloaded {} --".format(name))
    except Exception as e:
      yield False

  def addArgument(self, cmdName, varName, help="", var_type=str):
    """Add an argument to a function argument processor"""
    self.functions[cmdName].parser.add_argument(varName, help=help, type=var_type)
  
  def processCommand(self, cmd,username=""):
    """To run when we receive a command"""
    self.log.debug("RECV: {}".format(cmd))
    
    ##Get the command without the prefix (i.e "!")
    cmd = cmd.partition(self.prefix)[2].strip()

    self.log.debug("Resolved to {}".format(cmd))

    ##Separate the arguments from the command name
    com,sep,args = cmd.strip().partition(" ")
    
    ##Select the right object
    try:
      funcObject = self.functions[com]
    except KeyError:
      ##We don't know of the command
      self.log.info("Key {} not found".format(com))
      return "Command not found"

    try:
      ##Try to get the arguments from the string
      args = funcObject.parse([x for x in args.split(self.delimiter) if x!=''])

      ##Run the command
      running = self.run(com,args,username)
      for value in running:
        yield value
    except Exception as e:
      ##for if we failed to parse 
      yield "Error: {}".format(e)
      yield self.getHelp(cmd)
      
    except SystemExit:
      if com == "quit":
        sys.exit()
      yield self.getHelp(cmd)

  def run(self, com, args,username):
    """A wrapper to run the command"""
    r = self.runCommand(com, vars(args),username=username)
    for value in r:
      yield value

  def runCommand(self, com, arglist,username=""):
    """Run a command"""

    ##Get the function, arguments and if admin is needed
    funcObj = self.functions[com]
    x = []
    
    ##Organise the arguments into the order the function expects
    for i in funcObj.args:
      x.append(arglist[i])

    self.log.debug("Running {}({})".format(com, arglist))
    try:
      ##Make sure that if we need admin, the user has it
      if funcObj.admin:
        if username.lower() not in [x.lower() for x in self.admins]:
          self.log.warning("  User is not admin, failing")
          yield "Permission denied - User {} not admin".format(username)
          return
      ##Unpack the args and run the function
      y = funcObj.function(*x)
      self.log.debug("Running {} with arguments ({})".format(com, x))
      if y == None:
        ##In case func doesn't return anything
        yield None
      else:
        if type(y) == types.GeneratorType:
          ##Return func()
          for v in y:
            yield v
        else:
          yield y
    except Exception as e:
      self.log.error("Failed, {}".format(e))
      traceback.print_exc()
      yield self.getHelp(com)

  def getHelp(self, name):
    if name == "all":
      return self.getAllHelp()
    try:
      return self.parsers[name].format_help()
    except KeyError:
      return None

  def getAllHelp(self):
    """Get a string containing all usage strings"""

    x = ""
    for i in self.parsers:
      x += self.parsers[i].usage + "\n"
    yield x

  def isAdmin(self, username):
    yield "{} is{} an admin.".format(username, " not" if (not username.lower() in self.admins) else "")

  class Command:
    def __init__(self, name, parser, function, args=[], module="Builtin",admin=False):
      self.name = name
      self.parser = parser
      self.function = function
      self.module = module
      self.args = args
      self.admin = admin

    def parse(self, args):
      return self.parser.parse_args(args)

    def __repr__(self):
      return "{0.module}.{0.name}({1})".format(self, ", ".join(self.args))

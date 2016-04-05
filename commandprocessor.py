#!/usr/bin/env python3

import re
import argparse
import sys
import importlib
import traceback
from log import Log

class CommandProcessor:
  """A class to generically process commands, as defined by a list of commands and
     argparse parsers - used to extract arguments from a string"""

  def __init__(self, delimiter=",", prefix="!", modulePath=".", debug=False, admins=[]):
    self.log = Log()
    self.parsers = {}
    self.delimiter = delimiter
    self.functions = {}
    self.prefix = prefix
    ##Add the module path to PYTHONPATH
    sys.path.insert(0, modulePath)
    self.admins = admins
    if debug:
      self.log.setLevel(self.log.DEBUG)
      
  def addCommand(self, name, description="", usage="", func=None, arglist=[], 
                 need_admin=False):
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
          1 on Faliure"""

    #If the user doesn't provide a function, we can't do anything
    if not func:
      self.log.warning("No function provided for {}.".format(name))
      return 1

    #Check we haven't got the function already
    if not name in self.parsers:
      self.log.info("Adding {}({})".format(name, arglist))
      
      ##Add an argument parser for the function
      parser = argparse.ArgumentParser(description=description, usage=usage)
      ##Add the parser to our list
      self.parsers[name] = parser
      
      ##Add the arguments we want for this function
      for i in arglist:
        self.addArgument(name, i)
     
      ##Finally, add the function to our list
      self.addFunc(name, func, arglist, need_admin)
      return 1
    else:
      return 0

  def removeCommand(self, name):
    """Remove a command from the list"""
    try:
      del self.parsers[name]
      del self.functions[name]
    except:
      pass

  def loadModule(self, name):
    """Load an external module from modulepath"""
    try:
      self.log.info("Loading module {}".format(name))
      ##Try loading the module as i
      i = importlib.import_module(name)
      ##In case it's changed and was imported before, reload it 
      i = importlib.reload(i)
      ##Get a list of all the functions defined in the module
      funcs = dir(i)
      ##Don't import python's internal functions, like __name__ and __init__
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])

    
      ##Load the functions in
      for j in z:
        self.log.debug("Adding function {}.{}".format(name,j))
        try:
          ##this will actually get the function object, not just its name
          k = eval(j)
          ##Get the variables used in the function
          args = k.__code__.co_varnames
          ##Get the number of arguments the function expects
          num = k.__code__.co_argcount
          ##Throw the function and arguments over to our addCommand 
          self.addCommand(j.split(".")[-1], func=k, arglist=args[:num])
        except:
          ##In case it wasn't actually a function object
          pass
      self.log.info("Succesfully inserted {}".format(name))
      yield True
    except Exception as e:
      self.log.error("Failed with {}".format(e))
      yield False

  def unloadModule(self, name):
    """Unload an entire external module"""
    try:
      self.log.info("Unloading {}".format(name))
      i = importlib.import_module(name)
      funcs = dir(i)      
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])
      for j in z:         
        self.removeCommand(j.split(".")[-1])
      yield True  
      self.log.info("Succesfully unloaded {}".format(name))
    except Exception as e:
      yield False

  def addArgument(self, cmdName, varName, help="", var_type=str):
    """Add an argument to a function argument processor"""
    self.parsers[cmdName].add_argument(varName, help=help, type=var_type)

  def processCommand(self, cmd,username=""):
    """To run when we recieve a command"""
    self.log.debug("RECV: {}".format(cmd))
    
    ##Get the command without the prefix (i.e "!")
    cmd = cmd.partition(self.prefix)[2].strip()

    self.log.debug("Resolved to {}".format(cmd))

    ##Seperate the arguments from the command name
    com,sep,args = cmd.strip().partition(" ")
    
    ##Select the right parser
    try:
      parser = self.parsers[com]
    except KeyError:
      ##We don't know of the command
      self.log.info("Key {} not found".format(com))
      yield "Command not found"

    try:
      ##Try to get the arguments from the string
      args = parser.parse_args([x for x in args.split(self.delimiter) if x!=''])

      ##Run the command
      running = self.run(com,args,username)
      for value in running:
        yield value
    except Exception as e:
      ##for if we failed to parse 
      yield self.getHelp(cmd)
    

  def run(self, com, args,username):
    """A wrapper to run the command"""

    r = self.runCommand(com, vars(args),username=username)
    for value in r:
      yield value

  def runCommand(self, com, arglist,username=""):
    """Run a command"""

    ##Get the function, arguments and if admin is needed
    func,args,adm = self.functions[com]
    x = []
    
    ##Organise the arguments into the order the function expects
    for i in args:
      x.append(arglist[i])

    self.log.debug("Running {}({})".format(com, arglist))
    try:
      ##Make sure that if we need admin, the user has it
      if adm:
        if username not in self.admins:
          return "Permission denied - User {} not admin".format(username)
      
      ##Unpack the args and run the function
      y = func(*x)
      if y == None:
        ##In case func doesn't return anything
        yield "ok"
      else:
        ##Return func()
        for v in y:
          yield v
    except Exception as e:
      self.log.error("Failed, {}".format(e))
      traceback.print_exc()
      yield self.getHelp(com)

  def addFunc(self, funcname, func, argslist, need_admin):
    """Add a function to the command processor"""
    self.log.debug("Adding function: {} /({})".format(funcname, argslist))

    ##Associate the function name with the function
    self.functions[funcname] = [func, argslist, need_admin]

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
    return x

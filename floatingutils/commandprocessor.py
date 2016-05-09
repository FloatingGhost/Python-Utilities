#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'

import pyaml
import re
import argparse
import sys
import importlib
import traceback
from floatingutils.log import Log
import types
import typing
import threading
import queue
import asyncio
import atexit
from floatingutils.conf import YamlConf

class CommandProcessor(threading.Thread):
  """A class to generically process commands, as defined by a list of commands and
     argparse parsers - used to extract arguments from a string"""

  def __init__(self, configfile = "command-proc.conf"):
    super(CommandProcessor, self).__init__()
    self.log = Log()
    self.log.info("Command Processor Created")
    self.log.newline()
    self.log.info("CMDPROC INIT")
    self.log.line()
    self.log.incIndent()
    self.triggers = []
    self.log.info("Reading config...")
    
    self.config = YamlConf(configfile)

    
    self.callback = print
    self.log.info("Initilising command queue...")
    self.cmdQ = queue.Queue()
    self.log.info("Initilising output queue...")
    self.outputQ = queue.Queue()
    self.commands = {}
    self.loadedModules = ["Builtin"]

    self.log.info("Initilising requests...")
    self.stopReq = threading.Event()
    self.stopNOW = threading.Event()
    self.log.info("Setting config...")
    self.bot_name = self.config.getValue("bot", "name")
    self.bot_version = self.config.getValue("bot", "version")
    self.msg_prefix = self.config.getValue("bot", "msg_prefix")
    self.command_prefix = self.config.getValue("bot", "cmd_prefix")
    debug = self.config.getValue("bot", "debug_logging")
    
    module_path = self.config.getValue("modules", "path")
    self.module_path = module_path 
    sys.path.insert(0, module_path)

    initial_modules = self.config.getValue("modules", "load")

    inital_triggers = self.config.getValue("triggers")

    self.admins = self.config.getValue("admins")
    self.log.info("Read config.")
    
    self.log.info("Setting up modules...")
    for i in initial_modules:
      self.loadModule(i)

    self.log.info("Setting up triggers...")
    for i in inital_triggers:
      self.addTrigger(i, inital_triggers[i])

    self.log.info("Setting verbosity...")
    if debug:
      self.log.setLevel(self.log.DEBUG)
    sys.path.insert(0, module_path)
    self._addUtilityCommands()
    self.log.line()
    self.log.info("FINISHED CMDPROC INIT")   
    self.log.newline()
  
  def join(self, timeout=None):
    self.log.info("QUITTING")
    self.log.line("Q")
    self.stopReq.set()
    super(WorkerThread, self).join(timeout)
  
  def addCommand(self, function_name, function_object, help=None, module="Builtin"):
    """Add a command to the processor
       ARGS:
        function_name: The name you wish to call the function by, i.e "func" 
        function_object: The actual object to run when you call the command
    """
    self.log.info("Adding command {}".format(function_name))
    
    if function_name in self.commands:
      self.log.info("Command {} already registered. Overwriting")
    
    com = Command(function_name, function_object, help=help, module=module)
    if com.success:
      self.commands[function_name] = com
    else:
      self.log.info("Failed to add command")

  def removeCommand(self, function_name):
    if function_name in self.commands:
      del self.commands[function_name]
      self.log.info("Succesfully removed {}".format(function_name))
    else:
      self.log.info("Could not remove non-existent function {}".format(function_name))
  
  def addTrigger(self, trigger_text, replacement_text):
    """Add a text-based trigger - will send replacement_text when
       trigger_text is in a given message"""

    for trigger in self.triggers:
      if trigger.trigger == trigger_text:
        trigger.send_text = replacement_text
        return ("Modified trigger to {}".format(trigger))
        
    self.triggers.append(Trigger(trigger_text, replacement_text))
    self.log.info("Added {}".format(self.triggers[-1]))
    return ("Added -- {}".format(self.triggers[-1]))

  def writeConfig(self):
    self.log.info("Writing config...")
    trigs = {}
    for i in self.triggers:
      trigs[i.trigger] = i.send_text

    settings = {
        "bot" : {
          "name": self.bot_name,
          "version": self.bot_version,
          "msg_prefix": self.msg_prefix,
          "cmd_prefix": self.command_prefix,
          "debug_logging": False
        },
        "modules" : {
          "path": self.module_path,
          "load": self.loadedModules
        },
        "triggers": trigs,
        "ai": {
          "model_directory": "models"
        },
        "admins": self.admins
      } 
    self.log.info(settings)
    with open("command-proc.conf", "w") as f:
      f.write(pyaml.dump(settings))
    self.log.info("Written")

  def removeTrigger(self, txt):
    for trigger in self.triggers:
      if trigger.trigger == txt:
        self.triggers.remove(trigger)
        return ("Removed {}".format(trigger))

  def setCallback(self, function):
    """Set the function to run on function complete
       ARGS: function (python function)"""
    self.callback = function

  def _process(self, command):
    """Internal process command - parse the command and execute"""
    self.log.info("Processing request {}...".format(command[0]))
    #Remove trailing and preceeding spaces
    command = command[0]
    command[0] = command[0].strip()
    try: 
      #Check if it's a command or not
      if command[0][0] == self.command_prefix:
        #It's a command
        self._checkAgainstCommands(command)
      else:
        #We'll check it against the triggers
        self._checkAgainstTriggers(command)
    except IndexError:
      pass

  def _checkAgainstCommands(self, command):
    command,channel = command
    command = command[1:]
    command_name,sep,args = command.partition(" ")
    if command_name in self.commands:
      #Now we've verified, go ahead and run it
      try:
        cmd = self.commands[command_name].run(args)
        if type(cmd) == types.GeneratorType:
          for i in cmd:
            self.output([i, channel])
        else:
          self.output([cmd, channel])

      except ArgumentFormatError:
        self.output("Error running {} -- Argument format error")
    else:
      self.log.info("No command of name {} detected".format(command_name))

  def output(self, val):
    self.outputQ.put(val)
    if self.callback:
      self.callback(*val)

  def _checkAgainstTriggers(self, command):
    for i in self.triggers:
      if i.match(command[0]):
        self.output([i.send_text, command[1]])

  def getOutput(self):
    try:
      x = self.outputQ.get(False)
    except queue.Empty:
      return None
    return x

  def run(self):
    """Start the thread off"""
    self.log.info("Command processor thread starting...")
    while (not self.stopReq.isSet()) or self.cmdQ.qsize() != 0:
      if self.stopNOW.isSet():
        break
      try:
        toProcess = self.cmdQ.get(True, 0.5)
        self._process(toProcess)
      except queue.Empty:
        continue
      except Exception as e:
        self.log.error(e)
        traceback.format_exc(e)

    self.log.info("Stopping with qsize: {}".format(self.cmdQ.qsize()))
    self.log.info("Stopreq state: {}".format(self.stopReq.isSet()))
    self.log.info("Thread closed.")
    if dbot:
      dbot.saveandquit(False)
        

  def push(self, commandstring, discordChannel = None):
    """Add a command to the command queue - to be processed commands
       ARGS: commandstring (str) - the command to process"""
    self.log.info("Pushing command {}".format(commandstring))
    self.cmdQ.put([commandstring, discordChannel])
  
  def exit(self, now=False):
    """Quit the thread, cleanly exit"""
    admin = 1
    yield "Closing..."
    self.log.info("Exit request acknowledged, will exit.")
    self.stopReq.set()
    if (now):
      self.stopNOW.set()
    
  ##Module loading/unloading
  def loadModule(self, name):
    self.log.newline() 
    self.log.info("LOADING MODULE {}".format(name.upper())) 
    self.log.line()
    self.log.incIndent()
    try:
      ##Try loading the module as i
      yield("Importing {}...".format(name))
      i = importlib.import_module(name)
      ##In case it's changed and was imported before, reload it 
      self.log.debug("Reloading...")
      i = importlib.reload(i)
      ##Get a list of all the functions defined in the module
      self.log.debug("Getting functions...")
      funcs = dir(i)
      ##Don't import python's internal functions, like __name__ and __init__
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not (x.match(y) or y[-1]=="_")])
      self.log.debug("Loaded, adding functions...")
      self.log.incIndent()
      self.funcs = "Loaded functions:\n"
      ##Load the functions in
      for j in z:
        if type(eval(j)) == types.FunctionType:
          if "onimport" in j:
            self.log.info("Running import function...")
            eval(j)()
          elif "onexit" in j:
            atexit.register(eval(j))
          else:  
            self.addCommand(j.split(".")[1], eval(j), module=name)
            self.funcs += "!{}, ".format(j.split(".")[1])
      self.loadedModules.append(name)
    
      yield(self.funcs)
    except ImportError as ie:
      self.log.error("Could not find module {}".format(name))
      self.log.error(ie)
    except Exception as e:
      self.log.error("Unknown exception: {}".format(e)) 
    
  def unloadModule(self, module_name):
    yield "Unloading module {}".format(module_name)
    funcs = "( "
    for i in self.commands:
      if self.commands[i].module == module_name:
        self.removeCommand(i)
        funcs += i + ", "
    self.loadedModules.remove(module_name)
    self.log.info("Unloaded {} {} )".format(module_name, funcs))

  def lsmod(self):
    """List all currently loaded modules"""
    x = "Loaded modules: \n"
    x += "\n".join(self.loadedModules)
    return( x + "\n" )
  
  def getHelp(self, cmd=None):
    if cmd:
      if cmd in self.commands:
        return(self.commands[cmd].getHelp())
      else:
        return("Command does not exist")

  def listTriggers(self):
    return "\n".join([str(x) for x in self.triggers])

  def _addUtilityCommands(self):
    self.addCommand("lsmod", self.lsmod)
    self.addCommand("import", self.loadModule)
    self.addCommand("quit", self.exit)
    self.addCommand("help", self.getHelp)
    self.addCommand("mktrig", self.addTrigger)
    self.addCommand("rmtrig", self.removeTrigger)
    self.addCommand("lstrig", self.listTriggers)
    self.addCommand("writeconf", self.writeConfig)

class Command:
  def __init__(self, f_name, f_obj, help, module = "Builtin"):
    self.log = Log()
    self.log.newline()
    self.log.info("Creating command {}".format(f_name))
    self.log.line("-")
    self.name = f_name
    self.func = f_obj
    self.help = self.func.__doc__ or ""
    self.module = module
    self.admin_required = "admin" in self.func.__code__.co_varnames
    self.nargs = self.func.__code__.co_argcount
    self.defaults = self.func.__defaults__
    self.argdefault = {}
    if (self.defaults):
      self.noptargs = len(self.defaults) 
    else:
      self.noptargs = 0
    self.args = self.func.__code__.co_varnames[:self.nargs - self.noptargs]
    self.optargs = self.func.__code__.co_varnames[self.nargs-self.noptargs:
                                                  self.noptargs+1]
    self.hints = typing.get_type_hints(self.func) 
    if "self" in self.args:
      self.nargs -= 1
    self.args = tuple([x for x in self.args if x != "self"])
    for i in range(self.noptargs):
      self.argdefault[self.optargs[i]] = self.defaults[i]

    if self.nargs > 0:
      self.log.info("ARGS: " + ", ".join(self.args))
      self.log.info("OPTARGS: " + ", ".join(self.optargs))
      self.log.info("DEFAULTS: " + ", ".join(
                            ["{}={}".format(
                      i, self.argdefault[i]) for i in self.argdefault]))      
    else:
      self.log.info("No arguments")
    self.delim = ","
    self.NOSPLIT = "NOSPLIT" in self.func.__code__.co_varnames

    self.success = True
    self.log.line("-")
    self.log.info(self)

  def getHelp(self):
    h =  self.name + ":\n" + self.help 
    if self.nargs > 0:
      h += "\nARGS: " + ", ".join(self.args) + "\n" 
    if self.noptargs > 0:
      h +=  "\nOPTARGS: " + " , ".join(self.optargs)
    if "\n" not in h:
      h += " (No Arguments)"
    return h 

  def run(self, args, user_is_admin=False):
    if self.admin_required and not user_is_admin:
      self.log.warning("{} requires administrative permissions".format(self.name))
    self.log.newline()
    self.log.newline()
    self.log.line("+")
    if not self.NOSPLIT:
      args = self._formatArgs(args.split(self.delim))
    else:
      args = self._formatArgs([args])
    self.log.info("Running {} with args {}".format(self.name, args))
    output = self.func(**args)
    self.log.line("+")
    self.log.newline()
    self.log.newline()
    return output
  
  def _formatArgs(self, args):
    args = [x.strip() for x in args if x != '']
    processedArgs = {}
    allargs = self.args + self.optargs
    for i in range(self.nargs):
      arg = ""
      argn = allargs[i]
      if i >= len(args):
        arg = self.argdefault[argn]
      else:
        arg = args[i]
      if allargs[i] in self.hints:
        try:
          arg = self.hints[argn](arg)
        except ValueError as ex:
          raise ArgumentFormatError(ex)
      processedArgs[argn] = arg
    
    return processedArgs

  def __repr__(self):
    x = "\n\nCOMMAND DEFINITION ::- \n"
    return x+"\nCommand (\n Name: {}.{},\n Args: {},\n OptArgs: {}\n Admin: {}\n)\n".format(
            self.module, self.name, self.args, self.optargs, self.admin_required)


class Trigger:
  def __init__(self, trigger, send_text):
    self.trigger = trigger
    self.send_text = send_text

  def match(self, txt):
    regex = re.compile(".*{}.*".format(self.trigger))
    return regex.match(txt)
  
  def __repr__(self):
    return "{} -> {}".format(self.trigger, self.send_text)

class ArgumentFormatError(Exception):
  pass

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
import typing
import threading
import queue

class CommandProcessor(threading.Thread):
  """A class to generically process commands, as defined by a list of commands and
     argparse parsers - used to extract arguments from a string"""

  def __init__(self, delimiter=",", command_prefix="!", 
                     module_path=".", admins=[], debug=False):
    super(CommandProcessor, self).__init__()
    self.log = Log()
    self.log.info("Command Processor Created, prefix {}".format(command_prefix))
    self.log.newline()
    self.log.info("CMDPROC INIT")
    self.log.line()
    self.log.incIndent()
    if debug:
      self.log.setLevel(self.log.DEBUG)
    self.callback = print
    self.log.info("Initilising command queue...")
    self.cmdQ = queue.Queue()
    self.log.info("Initilising output queue...")
    self.outputQ = queue.Queue()
    self.commands = {}
    self.log.info("Initilising requests...")
    self.stopReq = threading.Event()
    self.stopNOW = threading.Event()
    self.log.info("Setting config...")
    self.command_prefix = command_prefix
    self.module_path = module_path
    self.admins = admins
    self.log.line()
    self.log.info("FINISHED CMDPROC INIT")   
    self.log.newline()

  
  def addCommand(self, function_name, function_object, help=None):
    """Add a command to the processor
       ARGS:
        function_name: The name you wish to call the function by, i.e "func" 
        function_object: The actual object to run when you call the command
    """
    self.log.info("Adding command {}".format(function_name))
    
    if function_name in self.commands:
      self.log.info("Command {} already registered. Overwriting")
    
    com = Command(function_name, function_object, help=help)
    if com.success:
      self.commands[function_name] = com
    else:
      self.log.info("Failed to add command")

  def setCallback(self, function):
    """Set the function to run on function complete
       ARGS: function (python function)"""
    self.callback = function

  def _process(self, command):
    """Internal process command - parse the command and execute"""
    self.log.info("Processing request {}...".format(command))
    
    #Remove trailing and preceeding spaces
    command = command.strip()
  
    #Check if it's a command or not
    if command[0] == self.command_prefix:
      #It's a command
      self._checkAgainstCommands(command)
    else:
      #We'll check it against the triggers
      self._checkAgainstTriggers(command)

  def _checkAgainstCommands(self, command):
    self.log.info("Detected command {}".format(command))
    command = command[1:]
    command_name,sep,args = command.partition(" ")
    if command_name in self.commands:
      self.log.info("Command name detected: {}".format(command_name))
      #Now we've verified, go ahead and run it
      try:
        cmd = self.commands[command_name].run(args)
        if type(cmd) == types.GeneratorType:
          for i in cmd:
            self.outputQ.put(i)
        else:
          self.outputQ.put(cmd)

      except ArgumentFormatError:
        self.outputQ.put("Error running {} -- Argument format error")
    else:
      self.log.info("No command of name {} detected".format(command_name))

  def _checkAgainstTriggers(self, command):
    pass

  def getOutput(self):
    return self.outputQ.get()

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

  def push(self, commandstring):
    """Add a command to the command queue - to be processed commands
       ARGS: commandstring (str) - the command to process"""
    self.log.debug("Pushing command {}".format(commandstring))
    self.cmdQ.put(commandstring)
    self.log.debug("Approx size: {}".format(self.cmdQ.qsize()))
  
  def exit(self, now=False):
    """Quit the thread, cleanly exit"""
    self.log.info("Exit request acknowledged, will exit.")
    self.stopReq.set()
    if (now):
      self.stopNOW.set()
    
class Command:
  def __init__(self, f_name, f_obj, help):
    self.log = Log()
    self.log.newline()
    self.log.info("Creating command {}".format(f_name))
    self.log.line("-")
    self.name = f_name
    self.func = f_obj
    self.help = help
    
    self.nargs = self.func.__code__.co_argcount
    self.defaults = self.func.__defaults__
    self.argdefault = {}
    if (self.defaults):
      self.noptargs = len(self.defaults) 
    else:
      self.noptargs = 0
    self.args = self.func.__code__.co_varnames[:self.nargs - self.noptargs]
    self.optargs = self.func.__code__.co_varnames[self.nargs-self.noptargs:
                                                  1+self.noptargs]
    self.hints = typing.get_type_hints(self.func) 

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
    
    self.success = True
    self.log.line("-")

  def run(self, args):
    self.log.newline()
    self.log.newline()
    self.log.line("+")
    args = self._formatArgs(args.split(self.delim))
    self.log.info("Running {} with args {}".format(self.name, args))
    output = self.func(**args)
    self.log.line("+")
    self.log.newline()
    self.log.newline()
    return output
  
  def _formatArgs(self, args):
    self.log.debug("Formatting arguments...")
    args = [x for x in args if x != '']
    self.log.line("=")
    self.log.debug("We recieved {} args".format(len(args)))
    processedArgs = {}
    allargs = self.args + self.optargs
    for i in range(self.nargs):
      self.log.debug("Trying to get arg '{}'".format(allargs[i]))
      arg = ""
      argn = allargs[i]
      if i >= len(args):
        arg = self.argdefault[argn]
      else:
        arg = args[i]
      self.log.debug("Got {}".format(args))   
      if allargs[i] in self.hints:
        self.log.debug("Casting to {}".format(self.hints[argn]))
        try:
          arg = self.hints[argn](arg)
        except ValueError as ex:
          raise ArgumentFormatError(ex)
        self.log.debug("Casted: {}".format(arg))
      processedArgs[argn] = arg
    
    self.log.line("=")
    return processedArgs

class Trigger:
  pass

class ArgumentFormatError(Exception):
  pass

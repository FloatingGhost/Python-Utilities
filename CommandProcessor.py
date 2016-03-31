#!/usr/bin/env python3

import re
import argparse

class CommandProcessor:
  def __init__(self, delimiter=",", prefix="!"):
    self.parsers = {}
    self.delimiter = delimiter
    self.functions = {}
    self.prefix = prefix

  def addCommand(self, name, description="", usage="", func=print, arglist=[]):
    if not name in self.parsers:
      parser = argparse.ArgumentParser(description=description, usage=usage)
      self.parsers[name] = parser
      
      if arglist == []:
        arglist = ["placeholder"]
      for i in arglist:
        self.addArgument(name, i)
     
      self.addFunc(name, func, arglist)
      print(self.parsers[name])
      return 1
    else:
      return 0

  def addArgument(self, cmdName, varName, help="", var_type=str):
    self.parsers[cmdName].add_argument(varName, help=help, type=var_type)

  def processCommand(self, cmd):
    print("  RECV: {}".format(cmd))
    print("    Partitioned: {}".format(cmd.partition(self.prefix)))
    cmd = cmd.partition(self.prefix)[2].strip()
    print("    Resolved to {}".format(cmd))
    com,sep,args = cmd.strip().partition(" ")
    print("Running {} with args {}".format(com, args))
    try:
      parser = self.parsers[com]
    except KeyError:
      print("No key")
      return None
    args = parser.parse_args(args.split(self.delimiter))
    return self.run(com,args)

  def run(self, com, args):
    return self.runCommand(com, vars(args))
  
  def runCommand(self, com, arglist):
    func,args = self.functions[com]
    x = []
    for i in args:
      x.append(arglist[i])
    try:
      return func(*x)
    except Exception as e:
      print("Failed, {}".format(e))
      return self.getHelp(com)

  def addFunc(self, funcname, func, argslist):
    self.functions[funcname] = [func, argslist]

  def getHelp(self, name):
    try:
      return self.parsers[name].format_help()
    except KeyError:
      return None

  def getAllHelp(self):
    return [self.getHelp(i) for i in self.parsers]

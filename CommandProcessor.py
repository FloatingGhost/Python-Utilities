#!/usr/bin/env python3

import re
import argparse

class CommandProcessor:
  def __init__(self, delimiter=","):
    self.parsers = {}
    self.delimiter = delimiter
    self.functions = {}

  def addCommand(self, name, description="", usage="", func=print, arglist=[]):
    if not name in self.parsers:
      parser = argparse.ArgumentParser(description=description, usage=usage)
      self.parsers[name] = parser
      for i in arglist:
        self.addArgument(name, i)
      self.addFunc(name, func, arglist)
      return 1
    else:
      return 0

  def addArgument(self, cmdName, varName, help="", var_type=str):
    self.parsers[cmdName].add_argument(varName, help=help, type=var_type)
    print("Added {}".format(cmdName))
  def processCommand(self, cmd):
    cmd = cmd[1:]
    print("Processing {}".format(cmd))
    com,sep,args = cmd.strip().partition(" ")
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
    return func(*x)

  def addFunc(self, funcname, func, argslist):
    self.functions[funcname] = [func, argslist]

  def getHelp(self, name):
    try:
      return self.parsers[name].format_help()
    except KeyError:
      return None

  def getAllHelp(self):
    return [self.getHelp(i) for i in self.parsers]

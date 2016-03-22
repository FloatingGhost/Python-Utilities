#!/usr/bin/env python3

import re
import argparse

class CommandProcessor:
  def __init__(self, delimiter=","):
    self.parsers = {}
    self.delimiter = delimiter

  def addCommand(self, name, description="", usage=""):
    if not name in self.parsers:
      parser = argparse.ArgumentParser(description=description, usage=usage)
      self.parsers[name] = parser
      return 1
    else:
      return 0

  def addArgument(self, cmdName, varName, help="", var_type=str):
    self.parsers[cmdName].add_argument(varName, help=help, type=var_type)

  def processCommand(self, cmd):
    com,sep,args = cmd.strip().partition(" ")
    try:
      parser = self.parsers[com]
    except KeyError:
      return None
    args = parser.parse_args(args.split(self.delimiter))
    return args

  def getHelp(self, name):
    try:
      return self.parsers[name].format_help()
    except KeyError:
      return None

  def getAllHelp(self):
    return [self.getHelp(i) for i in self.parsers]

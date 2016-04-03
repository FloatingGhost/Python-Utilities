#!/usr/bin/env python3

import re
import argparse
import sys
import importlib

class CommandProcessor:
  def __init__(self, delimiter=",", prefix="!", modulePath=".", debug=False, admins=[]):
    self.parsers = {}
    self.delimiter = delimiter
    self.functions = {}
    self.prefix = prefix
    sys.path.insert(0, modulePath)
    self.debug = debug
    self.admins = admins

  def addCommand(self, name, description="", usage="", func=None, arglist=[], 
                 need_admin=False):
    if not func:
      if self.debug:
        print("No function provided.")
      return 1

    if not name in self.parsers:
      if self.debug:
        print("Adding {}({})".format(name, arglist))
      parser = argparse.ArgumentParser(description=description, usage=usage)
      self.parsers[name] = parser
      
      for i in arglist:
        self.addArgument(name, i)
     
      self.addFunc(name, func, arglist, need_admin)
      return 1
    else:
      return 0

  def removeCommand(self, name):
    try:
      del self.parsers[name]
      del self.functions[name]
    except:
      pass

  def loadModule(self, name):
    try:
      i = importlib.import_module(name)
      i = importlib.reload(i)
      funcs = dir(i)
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])
      if self.debug:
        print(z)
      for j in z:
        try:
          k = eval(j)
          args = k.__code__.co_varnames
          num = k.__code__.co_argcount
          self.addCommand(j.split(".")[-1], func=k, arglist=args[:num])
        except:
          pass
      return True
    except Exception as e:
      if self.debug:
        print("Failed with {}".format(e))
      return False

  def unloadModule(self, name):
    try:
      i = importlib.import_module(name)
      funcs = dir(i)      
      x = re.compile("__[a-z]*__")
      z = ([("i.{}".format(y)) for y in funcs if not x.match(y)])
      for j in z:         
        self.removeCommand(j.split(".")[-1])
      return True  
    except Exception as e:
      return False
  def addArgument(self, cmdName, varName, help="", var_type=str):
    self.parsers[cmdName].add_argument(varName, help=help, type=var_type)

  def processCommand(self, cmd,username=""):
    if self.debug:
      print("  RECV: {}".format(cmd))
      print("    Partitioned: {}".format(cmd.partition(self.prefix)))
    cmd = cmd.partition(self.prefix)[2].strip()
    if self.debug:
      print("    Resolved to {}".format(cmd))
    com,sep,args = cmd.strip().partition(" ")
    try:
      parser = self.parsers[com]
    except KeyError:
      if self.debug:
        print("No key")
      return None
    try:
      args = parser.parse_args([x for x in args.split(self.delimiter) if x!=''])
    except:
      return self.getHelp(cmd)
    return self.run(com,args,username)

  def run(self, com, args,username):
    return self.runCommand(com, vars(args),username=username)
  
  def runCommand(self, com, arglist,username=""):
    func,args,adm = self.functions[com]
    x = []
    for i in args:
      x.append(arglist[i])
    if self.debug:
      print("Running {}({})".format(com, arglist))
    try:
      if adm:
        if username not in self.admins:
          return "Permission denied - User {} not admin".format(username)
      y = func(*x)
      if y == None:
        return "ok"
      else:
        return y
    except Exception as e:
      if self.debug:
        print("Failed, {}".format(e))
      return self.getHelp(com)

  def addFunc(self, funcname, func, argslist, need_admin):
    if self.debug:
      print("Adding function: {} / {}({})".format(funcname, func, argslist))
    self.functions[funcname] = [func, argslist, need_admin]

  def getHelp(self, name):
    if name == "all":
      return self.getAllHelp()
    try:
      return self.parsers[name].format_help()
    except KeyError:
      return None

  def getAllHelp(self):
    x = ""
    for i in self.parsers:
      x += self.parsers[i].usage + "\n"
    return x

#!/usr/bin/env python3

class Conf:
  def __init__(self, filename, sep=":"):
    self.filename = filename
    self.config = {}
    self.sep = sep
    self.readFile()
    self.extractConfig()

  def readFile(self):
    f = open(self.filename, "r")
    self.text = [x[:-1] for x in f.readlines() if x[:-1] != ""]
    f.close()     

  def extractConfig(self):
    lineno = 1
    for i in self.text:
      setting,sep,value = i.partition(self.sep)
      if setting in self.config:
        print("\nDuplicate setting '{}' (Line {})".format(setting, lineno)) 
      else:
        if setting == "":
          print("Empty setting name at Line {}".format(lineno))
        else:
          self.config[setting] = value
      lineno += 1

  def get(self, key):
    if key in self.config:
      return self.config[key]
    else:
      print("Setting '{}' not found!".format(key))
      return 0

  def set(self, key, value):
    if key == "":
      print("Non-empty keys only please! (value thrown: {})".format(value))
      return False
    else:
      self.config[key] = value
      return True

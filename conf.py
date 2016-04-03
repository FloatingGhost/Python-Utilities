#!/usr/bin/env python3

class Conf:
  def __init__(self, filename, sep=":", verbose=False):
    self.filename = filename
    self.verbose = verbose
    self.config = {}
    self.sep = sep
    self.readFile()
    self.extractConfig()

  def readFile(self):
    f = open(self.filename, "r")
    self.text = [x[:-1] for x in f.readlines() if x[:-1] != ""]
    f.close()     

  def writeFile(self, alternateFile=None):
    filename = self.filename
    if alternateFile:
      filename = alternateFile
    
    try:
      with open(filename, "w") as f:
        for i in sorted(self.config):
          f.write("{}:{}\n".format(i, self.config[i]))
    except Exception as e:
      print("ERROR: {}".format(e))
      return 1
    if self.verbose:
      print("\n{} Written succesfully".format(filename))

    return 0

  def extractConfig(self):
    lineno = 1
    for i in self.text:
      setting,sep,value = i.partition(self.sep)
      if setting in self.config:
        if self.verbose:
          print("\nDuplicate setting '{}' (Line {})".format(setting, lineno)) 
      else:
        if setting == "":
          if self.verbose:
            print("\nEmpty setting name (Line {})".format(lineno))
        else:
          if value == "":
            if self.verbose:
              print("\nEmpty setting value '{}' (Line {})".format(setting,lineno))
          else:
            self.config[setting] = value
      lineno += 1

  def getValue(self, key):
    if key in self.config:
      return self.config[key]
    else:
      if self.verbose:
        print("Setting '{}' not found!".format(key))
      return 0

  def getData(self, key):
    x=self.getValue(key)
    return eval(x)

  def setValue(self, key, value):
    if key == "":
      if self.verbose:
        print("Non-empty keys only please! (value thrown: {})".format(value))
      return False
    else:
      self.config[key] = value
      return True

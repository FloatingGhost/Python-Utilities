#!/usr/bin/env python3
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'


#-------------------#
#conf.py            #
#Wrappers for simple#
#yaml and key:value #
#configuration files#
#-------------------#

import yaml
from log import Log


class Conf:
  """Class for parsing simple (key sep value) format files"""

  def __init__(self, filename, sep=":"):
    self.log = Log()
    self.filename = filename
    self.log.info("Reading {}".format(filename))
    self.config = {}
    self.sep = sep
    self._readFile()
    self._extractConfig()
    self.log.info("Succesfully parsed {}".format(filename))
    
  def _readFile(self):
    """Read in the configuration file"""

    self.log.debug("Opening file {}".format(self.filename))
    ##Open the config file
    try:
      f = open(self.filename, "r")
    except FileNotFoundError:
      self.log.error("File '{}' not found!".format(self.filename))
    
    ##Read in each line, ignoring empty lines
    self.text = [x[:-1] for x in f.readlines() if x[:-1] != ""]
    self.log.debug("File read succesfully")
    ##Close the file
    f.close()     
    self.log.debug("{} closed".format(self.filename))

  def writeFile(self, alternateFile=None):
    """Write the changed configuration back to a file"""

    self.log.info("Writing config back to file")
    filename = self.filename
    ##Just in case the user wants to change location
    if alternateFile:
      filename = alternateFile
    self.log.info("Writing to {}".format(filename))

    try:
      with open(filename, "w") as f:
        for i in sorted(self.config):
          f.write("{}:{}\n".format(i, self.config[i]))
    except Exception as e:
      self.log.warning("An error occurred -- {}".format(e))
      return 1
    self.log.debug("{} Written succesfully".format(filename))
    return 0

  def _extractConfig(self):
    """Get all the key value pairs from the config file"""
    
    ##Keep track of line of debug purposes
    lineno = 1
    for i in self.text:
      ##Split the line by the seperator
      setting,sep,value = i.partition(self.sep)
      if setting in self.config:
        ##If we've already seen that key before
        self.log.warning("Duplicate setting '{}' (Line {})".format(setting, lineno)) 
      else:
        ##Check for empty setting name
        if setting == "":
          self.log.warning("Empty setting name (Line {})".format(lineno))
        else:
          ##Check for empty value
          if value == "":
            self.log.warning("Empty setting value '{}'(Line {})".format(setting,lineno))
          else:
            ##It all looks good
            self.config[setting] = value
      lineno += 1

  def getValue(self, key):
    """Get the value associated with a key"""

    if key in self.config:
      return self.config[key]
    else:
      ##If we can't find the key
      self.log.error("Setting '{}' not found!".format(key))
      return 0

  def getData(self, key):
    """Get the parsed value of a key - for lists and dicts"""
    x=self.getValue(key)
    return eval(x)

  def setValue(self, key, value):
    """Change the value of a setting"""

    if key == "":
      self.log.warning("Non-empty keys only please! (value thrown: {})".format(value))
      return False
    else:
      self.config[key] = value
      return True


class YamlConf:
  """Wrapper class to pYaml - useful for more complex configurations"""

  def __init__(self, filename):
    self.log = Log()
    self.log.info("Opening YAML config file '{}'".format(filename))
    try:
      with open(filename) as f:
        self.data = yaml.load(f.read())
    except yaml.YAMLError as e:
      self.log.error("File '{}' cannot be parsed!".format(filename))
      self.log.error("{}".format(e))
    self.log.info("{} YAML parsed succesfully".format(filename))
 
  def getValue(self, *keys):
    """Search through our data and find the specified key or subkey"""

    data = self.data
    ##Iterate through the key heirarchy 
    for i in keys:
      try:
        data = data.get(i)
      except KeyError:
        self.log.error("Key {} not found".format(self._formatKey(keys)))
        return None
    return data
  
  def _formatKey(self, keys):
    """Pretty print a key heirarchy"""

    form = ""
    for key in keys:
      form += "{} -> ".format(key)
    return form[:-3]

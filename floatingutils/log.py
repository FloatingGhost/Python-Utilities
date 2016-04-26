#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'


#----------------------------------#
#log.py                            #
#Wrapper to python's logging module#
#----------------------------------#

import logging
from logging.config import fileConfig
import sys
import os

class Log:
  """Simple wrapper to logging"""
  DEBUG = logging.DEBUG
  INFO  = logging.INFO
 
  def __init__(self, level=logging.INFO):
    ##Bootstrap config
    __location__ = os.path.realpath(os.path.join(os.getcwd(),
                                     os.path.dirname(__file__)))
    configFile = "config/logging.conf"
    configPath = os.path.join(__location__, configFile)
    try:
      fileConfig(configPath)
    except KeyError:
      print("ERROR IN LOGGING: Could not find {}".format(
                                                    configPath
                                                  ))
      sys.exit(1)

    self.log = logging.getLogger()

    self.setLevel(level)
  
    self.indent = 0

  def _indent(self):
    return " "*self.indent

  def incIndent(self):
    self.indent+=1

  def decIndent(self):
    self.indent -= 1
    if self.indent < 0:
      self.indent = 0

  def line(self, ch="=", n=30):
    self.log.info(ch*n)

  def newline(self):
    self.log.info("")
  
  def info(self, msg):
    """log a generic info message"""
    self.log.info(self._indent() + str(msg))

  def warning(self, msg):
    """log a warning - usually error-prone stuff"""
    self.log.warning(self._indent() + str(msg))

  def debug(self, msg):
    """debug logging - usually not logged unless level is high"""
    self.log.debug(self._indent() + str(msg))
 
  def error(self, msg):
    self.log.error(self._indent() + str(msg)) 
  def setLevel(self, val):
    self.log.setLevel(val)

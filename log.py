#!/usr/bin/env python3

#----------------------------------#
#log.py                            #
#Wrapper to python's logging module#
#----------------------------------#

import logging
from logging.config import fileConfig

class Log:
  """Simple wrapper to logging"""
  DEBUG = logging.DEBUG
  INFO  = logging.INFO
 
  def __init__(self, level=logging.INFO):
    fileConfig("logging.conf")
    
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

  def line(self, n=30):
    self.log.info("="*n)

  def newline(self):
    self.log.info("")
  
  def info(self, msg):
    """log a generic info message"""
    self.log.info(self._indent() + msg)

  def warning(self, msg):
    """log a warning - usually error-prone stuff"""
    self.log.warning(self._indent() + msg)

  def debug(self, msg):
    """debug logging - usually not logged unless level is high"""
    self.log.debug(self._indent() + msg)
 
  def error(self, msg):
    self.log.error(self._indent() + msg) 
  def setLevel(self, val):
    self.log.setLevel(val)

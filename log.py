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

  def info(self, msg):
    """log a generic info message"""
    self.log.info(msg)

  def warning(self, msg):
    """log a warning - usually error-prone stuff"""
    self.log.warning(msg)

  def debug(self, msg):
    """debug logging - usually not logged unless level is high"""
    self.log.debug(msg)
 
  def error(self, msg):
    self.log.error(msg) 
  def setLevel(self, val):
    self.log.setLevel(val)

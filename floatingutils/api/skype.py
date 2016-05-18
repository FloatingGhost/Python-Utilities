#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'

import Skype4Py as skype
import re
import sys
import threading
import traceback


import floatingutils.commandprocessor as commandprocessor
from floatingutils.log import Log


class Chat:
  """Represents a chat class in a skype client"""
  def __init__(self): 

    self.log = Log()    
    __builtins__["chat"] = self
    self.log.newline()
    self.log.info("SKYPE BOT INIT")
    self.log.line("+",40)
    self.log.incIndent()
    self.log.newline()
    self.log.info("SKYPE4PY STARTUP")
    self.log.line()
    self.log.incIndent()
    self.s = skype.Skype()
    ##Connect to the API
    self.s.Attach()
    self.log.decIndent()
    self.log.line()
    self.log.info("SKYPE4PY STARTED")
    self.log.newline()
    ##Set initial variables
    self.lastMessage = None
    
    ##Create a processor for all possible commands
    self.cmdProc = commandprocessor.CommandProcessor()

    ##Try to connect to the chat
    try:
      self.chat = self.s.ActiveChats[0]
    except Exception as e:
      print("Cloud chat not supported! {}".format(e))
      sys.exit(1)
  
    ##Allow for some twiddling
    self.lastMessage = self.chat.Messages[0]
 
    ##Alert users to the bot presence
    self.log.line("+", 40)
    self.log.info("FINISHED SKYPE BOT INIT")
    self.log.newline()

  def send(self, msg):
    """Send a message to the chat"""
    if msg != None and msg != "" and type(msg) != type(True):
      self.chat.SendMessage(">>>"+msg)

  def processMessage(self):
    """Figure out what to do with the last received message"""
    if ">>>" not in self.lastMessage.Body:
      self.log.info("Processing {}".format(self.lastMessage.Body))
      self.cmdProc.push([self.lastMessage.Body, None])
    
  def mainloop(self):
    self.log.info("Starting mainloop...")
    self.cmdProc.start()
    threading.Thread(target=self.getOutput).start()
    self.log.info("Started thread.")
    while 1:
      try:
        newmsg = self.chat.Messages[0]
        if self.lastMessage != newmsg:
          self.lastMessage = newmsg
          self.processMessage()
      except KeyboardInterrupt:
        sys.exit()
   
  def addCommand(self, cmdName, func):
    self.cmdProc.addCommand(cmdName, func)

  def getAllBy(self, handle):
    return [i.Body for i in self.chat.Messages if str(i.FromHandle).lower() == handle]

  def getOutput(self):
    self.log.info("Starting output thread...")
    while True:
      x = (self.cmdProc.getOutput())
      if type(x) == list:
        self.send(x[0])
      else:
        self.send(x)

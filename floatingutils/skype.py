#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'

import Skype4Py as skype
import re
import floatingutils.commandprocessor as commandprocessor
import sys
import threading
from floatingutils.log import Log
import traceback
class Chat:
  """Represents a chat class in a skype client"""
  def __init__(self, cmd="!", botname="Generic Bot", msg_prefix="BOT: ", 
                processFunction=None, modulePath=".", admins=[], init_modules=None,
                init_triggers=None, debug=False):

    self.log = Log()    
    if debug:
      self.log.info("DEBUGGING ON")
      self.log.setLevel(self.log.DEBUG)
    ##For other modules
    __builtins__["chat"] = self

    self.log.newline()
    self.log.info("SKYPE BOT INIT")
    self.log.line("+",40)
    self.log.incIndent()
    self.log.info("Starting {}".format(botname))
    self.log.debug("Command prefix is set to '{}'".format(cmd))
    self.log.debug("Message Prefix is set to '{}'".format(msg_prefix))
    self.log.debug("Module to load: {}".format(init_modules))
    ##Create the skype instance
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
    self.cmd = cmd
    self.botname = botname
    self.hooks = []
    self.commands = []
    self.msg_prefix = msg_prefix
    self.processFunction = processFunction 
    
    ##Create a processor for all possible commands
    self.cmdProc = commandprocessor.CommandProcessor(",", cmd, modulePath,
                    admins=admins,debug=debug)

    ##Try to connect to the chat
    try:
      self.chat = self.s.ActiveChats[0]
    except Exception as e:
      print("Cloud chat not supported! {}".format(e))
      sys.exit(1)
  
    ##Allow for some twiddling
    self.lastMessage = self.chat.Messages[0]
 
    ##Alert users to the bot presence
    self.send("Starting {}".format(botname))
    self.log.info("Adding admin commands...")
    ##Initial setup
    self.addCommand("setprefix", self.setPrefix)

    ##Load any default modules
    if init_modules:
      self.log.info("Adding initial modules...")
      self.send("Initialising modules...")
      for i in init_modules:
        self.lastMessage.Body = "!import {}".format(i)
        self.processMessage()
    
    if init_triggers:
      self.log.info("Adding initial triggers...")
    self.send("Initialisation successful!")

    self.log.line("+", 40)
    self.log.info("FINISHED SKYPE BOT INIT")
    self.log.newline()

  def setPrefix(self, pre):
    """Set the icon for the bot to send with"""
    self.msg_prefix = pre
    self.send("Set!")

  def send(self, msg):
    """Send a message to the chat"""
    if msg != None and msg != "" and type(msg) != type(True):
      self.chat.SendMessage("{}: {}".format(self.msg_prefix, msg))

  def processMessage(self):
    """Figure out what to do with the last received message"""
    if self.msg_prefix not in self.lastMessage.Body:
      self.log.info("Processing {}".format(self.lastMessage.Body))
      self.cmdProc.push(self.lastMessage.Body)
    
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
      self.send(self.cmdProc.getOutput())


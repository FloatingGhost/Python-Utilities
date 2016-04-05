#!/usr/bin/env python3
import Skype4Py as skype
import re
import commandprocessor
import sys
import threading
from log import Log
class Chat:
  """Represents a chat class in a skype client"""
  def __init__(self, cmd="!", botname="TestBot", msg_prefix="BOT: ", 
                processFunction=None, modulePath=".", admins=[], init_modules=[]):

    self.log = Log()    
    self.log.setLevel(self.log.DEBUG)
    self.log.info("Starting {}".format(botname))
    self.log.debug("Command prefix is set to '{}'".format(cmd))
    self.log.debug("Message Prefix is set to '{}'".format(msg_prefix))
    ##Create the skype instance
    self.s = skype.Skype()
    
    ##Connect to the API
    self.s.Attach()

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
                    admins=admins,debug=True)

    ##Try to connect to the chat
    try:
      self.chat = self.s.ActiveChats[0]
    except Exception as e:
      print("Cloud chat not supported! {}".format(e))
      sys.exit(1)

    ##Alert users to the bot's presence
    self.send("Starting {}".format(botname))

    ##Initial setup
    self.addCommand("setprefix", "Set the bot's prefix", "setprefix [prefix]",
                    self.setPrefix, ["prefix"])
    self.addCommand("list", "list triggers", "list", self.listTriggers)
    self.addCommand("trig", "Add a trigger", "trig x y", self.addTrigger, ["t", "tr"])

    ##Load any default modules
    if init_modules != []:
      self.send("Initialising modules...")
      for i in init_modules:
        self.cmdProc.loadModule(i)
      self.send("Initalisation succesful!")

  def setPrefix(self, pre):
    """Set the icon for the bot to send with"""
    self.msg_prefix = pre
    self.send("Set!")

  def getHelp(self, cmd):
    """Get the help text for cmd"""

    if cmd == "":
      helpText = "Currently installed commands: "
      for i in (self.cmdProc.getAllHelp()):
        helpText += "\n{}".format(i)
      self.send(helpText)
    else:
      self.send(self.cmdProc.getHelp(cmd))
  
  def send(self, msg):
    """Send a message to the chat"""
    if msg != None and msg != "" and type(msg) != type(True):
      self.chat.SendMessage("{}: {}".format(self.msg_prefix, msg))

  def processMessage(self):
    """Figure out what to do with the last recieved message"""

    m = self.lastMessage
    n = m.Body.strip()
    if n[0] == self.cmd:
      #If the message starts with our command prefix, process it as a command
      self.processAsCommand()
    else:
      #If not, check it against the text triggers
      self.processAsText()
    
  def processAsCommand(self):
    """Figure out what command the user wants to run"""

    x=(self.cmdProc.processCommand(self.lastMessage.Body.strip(),
                                   username=self.lastMessage.FromHandle))
    if x:
      for v in x:
        self.send(v)
    else:
      self.send("Command not found :c")

  def processAsText(self):
    m = self.lastMessage
    n = m.Body.strip()
    for i in self.hooks:
      if i.match(n):
        self.send(str(i))
    if self.processFunction:
      if "Starting {}".format(self.botname) not in n:
        qq = (self.processFunction(n))
        if qq:
          self.send(qq)

  def addTrigger(self, triggerText, text, substring_match=False):
    self.hooks.append(self.Trigger(triggerText, text, self.msg_prefix, substring_match))
    return "Done!"

  def listTriggers(self):
    x = "The text triggers I currently have are:\n"
    for i in self.hooks:
      x += "{}\n".format(i.me())
    return (x)

  def mainloop(self):
    while 1:
      try:
        newmsg = self.chat.Messages[0]
        if self.lastMessage != newmsg:
          self.lastMessage = newmsg
          self.processMessage()
      except KeyboardInterrupt:
        sys.exit()
  
  def addCommand(self, cmdName, desc, usage, func, arglist=[],need_admin=False):
    self.cmdProc.addCommand(cmdName, desc, usage, func, arglist,need_admin=need_admin)

  def getAllBy(self, handle):
    return [i.Body for i in self.chat.Messages if str(i.FromHandle).lower() == handle]

  class Trigger:
    def __init__(self, trigger, text, bot_prefix, substring_match=False):
      self.text = text
      self.trigger = trigger.strip().lower()
      self.sub = substring_match
      self.msg_prefix = bot_prefix

    def match(self, i):
      i = i.strip().lower()
      if self.msg_prefix in i:
        return False
      if len(self.trigger.split(" ")) > 1:
        return self.trigger in i

      if self.sub:
        return (self.trigger in i)
      else:
        return (self.trigger in i.strip().lower().split(" "))    
 
    def me(self):
      return "{} -> {}".format(self.trigger, self.text)
 
    def __repr__(self):
      return self.text

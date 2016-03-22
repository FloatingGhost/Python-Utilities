#!/usr/bin/env python3
import Skype4Py as skype
import re
import CommandProcessor
import sys

class Chat:
  def __init__(self, cmd="!", botname="TestBot"):
    self.s = skype.Skype()
    self.s.Attach()
    self.lastMessage = None
    self.cmd = cmd
    self.botname = botname
    self.hooks = []
    self.commands = []
    self.cmdProc = CommandProcessor.CommandProcessor()
    try:
      self.chat = self.s.ActiveChats[0]
    except Exception as e:
      print("Cloud chat not supported! {}".format(e))


  def send(self, msg):
    self.chat.SendMessage(msg)

  def processMessage(self):
    m = self.lastMessage
    n = m.Body.strip()
    if n[0] == self.cmd:
      self.processAsCommand()
    else:
      self.processAsText()

  def processAsCommand(self):
    self.cmdProc.processCommand(self.lastMessage.Body.strip())

  def processAsText(self):
    m = self.lastMessage
    n = m.Body.strip()
    for i in self.hooks:
      if i.match(n):
        self.send(str(i))

  def addTrigger(self, triggerText, text, substring_match=False):
    self.hooks.append(self.Trigger(triggerText, text, substring_match))

  def mainloop(self):
    self.send("Starting {}".format(self.botname))
    while 1:
      try:
        newmsg = self.chat.Messages[0]
        if self.lastMessage != newmsg:
          self.lastMessage = newmsg
          self.processMessage()
      except KeyboardInterrupt:
        sys.exit()

  class Trigger:
    def __init__(self, trigger, text, substring_match=False):
      self.text = text
      self.trigger = trigger.strip().lower()
      self.sub = substring_match

    def match(self, i):
      if self.sub:
        return (self.trigger in i)
      else:
        return (self.trigger == i.strip().lower())    
  
    def __repr__(self):
      return self.text

#!/usr/bin/env python3
import Skype4Py as skype
import re
from parse import *
import parse

class Chat:
  def __init__(self, cmd="!"):
    self.s = skype.Skype()
    self.s.Attach()
    self.lastMessage = None
    self.cmd = cmd
    self.hooks = []
    self.commands = []
    try:
      self.chat = self.s.ActiveChats[0]
    except:
      print("Cloud chat not supported!")


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
    pass

  def processAsText(self):
    m = self.lastMessage
    n = m.Body.strip()
    for i in self.hooks:
      if i.match(n):
        self.send(str(i))

  def addTrigger(self, triggerText, text, substring_match=False):
    self.hooks.append(Trigger(triggerText, text, substring_match))

  def mainloop(self):
    while 1:
      newmsg = self.chat.Messages[0]
      if self.lastMessage != newmsg:
        self.lastMessage = newmsg
        self.processMessage()


  class Command:
    def __init__(self, cmd, func, helptext, syntax=''):
      self.cmd = cmd
      self.func = func
      self.helptext = helptext
      self.syntax = syntax
      self.cmdparse = parse.compile(syntax)


    def run(self, cmdtext):
      pass
       
    def _run(self, args=None):
      if args:
        self.func(*args)
      else:
        self.func()

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

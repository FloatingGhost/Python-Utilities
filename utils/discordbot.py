#!/usr/bin/env python3
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'


import discord
import asyncio
import requests
from log import Log
from conf import YamlConf
import json
from commandprocessor import CommandProcessor 
import re
log = Log()


client = discord.Client()

class Discord:
  def __init__(self, cli, cmd_prefix="!", botname="Discord bot",
                     msg_prefix="BOT: ", modulePath=".", admins=["FloatingGhost"],
                     init_modules=None, init_triggers=None):

    self.triggers = []                  
    self.bot_prefix = msg_prefix
    self.cmd_prefix = cmd_prefix
    self.botname = botname
    self.conf = YamlConf("discord.login")
    self.cmd = CommandProcessor(prefix=cmd_prefix, 
               modulePath=modulePath, admins=admins)

    self.admins = admins
    log.info("Logging in email {}...".format(self.conf.getValue("login", "email")))
    log.info("Logged in!")

    if init_triggers:      
      for i in init_triggers:
        self.triggers.append(self.Trigger(i, init_triggers[i], self.bot_prefix))
    
    if init_modules:
      for i in init_modules:
        x = self.cmd.processCommand("!import {}".format(i))
        for j in x:
          pass
    self.cli = cli 
    
    self.addAdminCommands()

  def addAdminCommands(self):
    log.info("Adding admin commands...")
    self.cmd.addCommand("trig", func=self.addTrigger, arglist=["trig", "trigger"])
    self.cmd.addCommand("rmtrig", func=self.rmtrig, arglist=["trig"])
    self.cmd.addCommand("lsadmin", func=self.lsadmin)
    self.cmd.addCommand("setprefix", func=self.setprefix, arglist=["pref"])

  def setprefix(self, p):
    self.bot_prefix = p
    return "Set!"

  def lsadmin(self):
    x = "Admins are:\n"
    for i in self.admins:
      x += i + "\n"
    return x

  def rmtrig(self, trig):
    for i in self.triggers:
      if i.match(trig):
        self.triggers.remove(i)
    return "Removed."
  def addTrigger(self, trig, trigger):
    self.triggers.append(self.Trigger(trig, trigger, self.bot_prefix))
    return "ADDED!"
   
  async def processCommand(self, cmd):
    if cmd.author != self.cli.user and cmd.content[0] == self.cmd_prefix:
      content = cmd.content
      user = cmd.author
      x= self.cmd.processCommand(content, username=str(user).split("#")[0])
      for i in x:
        await self.send(i,cmd.channel)
      return 0
    else:
      if cmd.author != self.cli.user:
        for i in self.triggers:
          if i.match(cmd.content):
            await self.send(str(i), cmd.channel)
  
  async def send(self, msg, channel=None):
    #Strip all bare lines
    if msg != None:
      msg = [x for x in msg.split("\n") if len(x) >1]
      y = ""
      for i in msg:
        y += i + "\n"
      msg = y
      if msg not in [None, True, False, "","\n"] and len(msg)>1:
        log.info("Sending {} to {}".format(msg, channel))
        await self.cli.send_message(channel, self.bot_prefix + " " + msg)

  def mainloop(self):
    log.info("Starting mainloop")
    
    self.cli.run(self.conf.getValue("login", "email"),
                    self.conf.getValue("login", "password"))

  class Trigger:
    def __init__(self, trigger, text, bot_prefix, substring_match=False):
      self.text = text
      self.trigger = trigger
      self.sub = substring_match
      self.msg_prefix = bot_prefix

    def match(self, i):
      try:
        i = i.strip()
        if self.msg_prefix in i:
          return False
        if len(self.trigger.split(" ")) > 1:
          return self.trigger in i
        log.info("{}, {}".format(i, self.trigger))
        reg = re.compile(self.trigger)
        if reg.match(i):
          return True
        return False
      except:
        return False

    def me(self):
      return "{} -> {}".format(self.trigger, self.text)

    def __repr__(self):
      return self.text

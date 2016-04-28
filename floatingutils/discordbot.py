#!/usr/bin/env python3
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'

import os
import discord
import asyncio
import requests
from floatingutils.log import Log
from floatingutils.conf import YamlConf
from floatingutils.commandprocessor import CommandProcessor 
import threading
import json
import re
import pyaml
import sys
import pickle
import atexit
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
    self.cmd = CommandProcessor(command_prefix=cmd_prefix, 
               module_path=modulePath, admins=admins)
    self.path = modulePath
    self.admins = admins
    self.init_modules = init_modules
    
    log.info("Logging in email {}...".format(self.conf.getValue("login", "email")))
    log.info("Logged in!")
    log.setLevel(log.DEBUG)
    atexit.register(self.saveandquit, True)
    self.cli = cli
    try:
      with open("msgs.bin", "rb") as f: 
        self.cli.messages = pickle.load(f)
    except Exception as e:
      log.error(e)

  def saveandquit(self, restart):
    log.info("Restarting...")
    trigs = {}
    for i in self.triggers:
      trigs[i.trigger] = i.text

    settings = {
                "bot": {
                  "name": self.botname,
                  "msg_prefix": self.bot_prefix,
                  "cmd_prefix": self.cmd_prefix,
                  "debug_logging": False 
                },
                "modules": {
                  "path": self.path,
                  "load": self.init_modules
                },
                "triggers": trigs,
                "admins": self.admins,
                "ai":{"model_directory":"models"}
              }
    with open("discord-config.conf", "w") as f:
      f.write(pyaml.dump(settings))
    with open("msgs.bin", "wb") as f:
      pickle.dump(self.cli.messages,f)
    log.info("Closing client...")
    self.cli.close()
    
    if restart:
      log.info("Restarting...")
      os.system("python DiscordBot.py")
    else:
      sys.exit()

  def setprefix(self, p):
    self.bot_prefix = p
    return "Set!"

   
  async def processCommand(self, cmd):
    if cmd.author != self.cli.user:
      self.cmd.push([cmd.content, cmd.channel]) 
 
  async def send(self, msg, channel=None):
    #Strip all bare lines
    if msg not in [None, True, False]:
      msg = [x for x in msg.split("\n") if len(x) >1]
      y = ""
      for i in msg:
        y += i + "\n"
      msg = y
      if msg not in [None, True, False, "","\n"] and len(msg)>1:
        if len(msg) > 1000:
          msg = msg[:1000]
        log.info("Sending {} to {}".format(msg, channel))
        await self.cli.send_message(channel, self.bot_prefix + " " + msg)
 
  def mainloop(self):
    log.info("Starting mainloop")
    
    try: 
      self.cmd.start()
      loop = asyncio.get_event_loop()
      loop.run_until_complete(self.cli.run(self.conf.getValue("login", "email"),
                 self.conf.getValue("login", "password")))
    except Exception as ex:
      #self.saveandquit(True)
      log.error(ex)

#!/usr/bin/env python3
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'


import discord
import asyncio
import requests
from log import Log
from conf import YamlConf
import json

log = Log()


client = discord.Client()
class Discord:
  def __init__(self):
    self.conf = YamlConf("discord.login")
    log.info("Logging in email {}...".format(self.conf.getValue("login", "email")))
    log.info("Logged in!")
    self.mainloop()
  @client.event
  async def on_ready():
    log.info("Ready!")
    log.info("Logged in as {}".format(client.user.name))
  def mainloop(self):
    log.info("Starting mainloop")
    
    client.run(self.conf.getValue("login", "email"),
                    self.conf.getValue("login", "password"))

#!/usr/bin/env python3

from floatingutils.log import Log
import requests
import sys

log = Log()

class Client:
  def __init__(self, IP:str, PORT:int, protocol:str="http"):
    self.ip = IP
    self.port = PORT
    self.socket = "{}://{}:{}".format(protocol, IP, PORT)
      
    log.info("Connecting to server {}".format(self.socket))
  
  def post(self, path, data:dict={}):
    try:
      data["SESSION_KEY"] = self.session
    except AttributeError:
      pass

    try:
      r = requests.post("{}/{}".format(self.socket, path), data=data)
    except requests.exceptions.ConnectionError:
      log.error("Server did not respond.")
      sys.exit(1)
    return self._processResponse(r.text)

  def getServerPub(self):
    return self.server_rsa or None

  def getSessionKey(self):
    return self.session or None

  def _processResponse(self, plain_resp, sep="//////"):
    keyvals = [x for x in (plain_resp.strip().split(sep)) if x != '']
    values = {}
    for i in keyvals:
      if i[:1] == "\n":
        i = i[1:]
      if i[-1:] == "\n":
        i = i[:-1]
      key,sep,val = i.partition("\n")
      if key != "":
        values[key] = val
    if "RSA_PUBLIC" in values:
      self.server_rsa = values["RSA_PUBLIC"]

    if "SESSION_KEY" in values:
      self.session = values["SESSION_KEY"]
  
    return values

  

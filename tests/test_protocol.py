#!/usr/bin/env python3

from floatingutils.network.protocol import Protocol
from floatingutils.log import Log
from nose.tools import nottest

log = Log()

class MemeProto(Protocol):
  pass

meme = MemeProto("MEME")
meme.addCode(100, "OK")
meme.addCode(200, "FAIL")
meme.addCode(500, "PLSADD")

meme.addCode(300, "HELLO")
meme.addCode(301, "BYE")

meme.addExpectedResponse("HELLO", 100)
meme.addExpectedResponse("BYE", 100)

@nottest
def memeFunc(args):
  log.info(args)
  return sum(args["MEME"])

meme.addProcessFunction(500, memeFunc)

def test_code():
  assert(meme.getCode("OK") == 100)
  assert(meme.getCode("FAIL") == 200)
  assert(meme.getCode("MEME") == -1)
  assert(meme.getMsg(100) == "OK")
  assert(meme.getMsg(200) == "FAIL")
  assert(meme.getMsg(999) == "INVALID_STATUS")

def test_response():
  assert(meme.process({"PROTOCOL":"MEME", "STATUS":500,
                       "MEME":[1,2,3]})["MESSAGE"] == 6)
  
  assert(meme.process({"PROTOCOL":"MEME", "STATUS":500})["STATUS"] == meme.getCode(
          "NO_YOU_FAGGOT_THATS_WRONG"))


  assert(meme.process({"PROTOCOL":"MEME", "STATUS":300})["STATUS"] == 100)


class Handshake(Protocol):
  pass

hsk = Handshake("3way")
hsk.addCode(100, "AUTH_SUCC")
hsk.addCode(200, "AUTH_FAIL")

hsk.addCode(101, "AUTH_REQ")
hsk.addCode(102, "AUTH_CHAL")
hsk.addCode(103, "AUTH_ANS")
hsk.addCode(104, "AUTH_CHECK")

@nottest
def hskReq(args):
  log.info("REQUESTING HANDSHAKE")
  return {"CHALLENGE":3}

@nottest
def hskChall(args):
  log.info("CHALLENGING CLIENT") 
  return {"ANSWER":args["CHALLENGE"]+1, "CHALLENGE":6}

@nottest
def hskAns(args):
  log.info("CHALLENGING SERVER")
  if (args["ANSWER"] != 4):
    STATUS = 200
  else:
    STATUS = None
  return {"ANSWER":args["CHALLENGE"]+1, "STATUS":STATUS}

@nottest
def hskAuth(args):
  log.info("FINALIZING HANDSHAKE")
  if (args["ANSWER"] != 7):
    STATUS = 200
    KEY = None
  else:
    STATUS = 100
    KEY = "YaYY"

  return {"STATUS":STATUS, "SESSIONKEY":KEY}

hsk.addProcessFunction(101, hskReq)
hsk.addProcessFunction(102, hskChall)
hsk.addProcessFunction(103, hskAns)
hsk.addProcessFunction(104, hskAuth)

hsk.addExpectedResponse(101, 102)
hsk.addExpectedResponse(102, 103)
hsk.addExpectedResponse(103, 104)
hsk.addExpectedResponse(104, 100)

def test_hsk():
  o = hsk.process({"STATUS":101, "PROTOCOL":"3WAY"})
  for i in range(3):
    o = hsk.process(o)
  log.info("Key recieved: {}".format(o["SESSIONKEY"]))
  assert(o["SESSIONKEY"] == "YaYY")

#HTTP

import os
from binascii import hexlify
@nottest
def http_GET(args):
  log.info("HTTP GET {} ".format(args["PATH"]))
  if os.path.exists(args["PATH"]):
    with open(args["PATH"], "r") as f:
      return {"STATUS":200, "FILE":hexlify(f.read())}
  else:
    return {"STATUS":404}  
class HTTP(Protocol):
  pass

http = HTTP("http")

http.addCode(100, "GET_REQ")
http.addCode(200, "OK")
http.addCode(404, "NOT_FOUND")
http.addCode(400, "ERROR")

http.addProcessFunction(100, http_GET)

def test_http():
  o = http.process({"PROTOCOL":"HTTP", "STATUS":100, "PATH":"test_yaml.py"})
  log.info(o)

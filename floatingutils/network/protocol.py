#!/usr/bin/env python3

from floatingutils.log import Log

log = Log()


class Protocol:
  """a nice widdle class for to hjaelp Protocol"""

  def __init__(self, name):
    log.info("Creating protocol {}".format(name))
    self.name = name
    self.codes = {}
    self.revCodes = {}
    self.expectedResponses = {}
    self.processFunctions = {}
    self.addCode(-1, "UNKNOWN_ERROR")
    self.addCode(-2, "WRONG_PROTOCOL")
    self.addCode(-3, "NO_YOU_FAGGOT_THATS_WRONG")
    self.addCode(-4, "NOT_IMPLEMENTED")
  def addCode(self, code:int, msg:str):
    log.info("Adding code {} = {}".format(code, msg))
    self.codes[code] = msg
    self.revCodes[msg] = code

  def getCode(self, msg:str):
    if msg in self.revCodes:
      return self.revCodes[msg]
    else:
      return -1

  def getMsg(self, code:int):
    if code in self.codes:
      return self.codes[code]
    else:
      return "INVALID_STATUS"

  def addExpectedResponse(self, message:str, expected:int):
    if isinstance(message, str):
      message = self.getCode(message)
    log.info("Adding Response {} -> {}".format(message, expected))
    self.expectedResponses[message] = expected

  def addProcessFunction(self, code:str, func):
    self.processFunctions[code] = func

  def getExpectedResponse(self, code):
    if code in self.expectedResponses:
      log.info("Response: {} -> {}".format(code, self.expectedResponses[code]))
      return self.expectedResponses[code]
    else:
      return None

  def process(self, data:dict):
    try:
      if(data["PROTOCOL"] != self.name.upper()):
        return self.protocolFormat({"STATUS":self.getCode("WRONG_PROTOCOL")})
      code = data["STATUS"]
      if code in self.processFunctions:
        return self.protocolFormat(self.processFunctions[code](data),
                                   code
                                    )
    except AssertionError as ex:
      log.error(ex)
      log.error(data)
      return self.protocolFormat({"STATUS":self.getCode("UNKNOWN_ERROR")})
    except KeyError:
      return self.protocolFormat({"STATUS":self.getCode("NO_YOU_FAGGOT_THATS_WRONG")})
    except Exception as ex :
      log.error(ex) 
      return self.protocolFormat({"STATUS":self.getCode("UNKNOWN_ERROR")})
    
    x = self.getExpectedResponse(data["STATUS"])
    if x:
      return self.protocolFormat({"STATUS":x})
    return self.protocolFormat({"STATUS":self.getCode("NOT_IMPLEMENTED")})

  def protocolFormat(self, data:dict, code:int=None):
    if isinstance(data, dict):
      data["PROTOCOL"] = self.name.upper()
      if "STATUS" not in data or data["STATUS"] == None: 
        if code:
          if self.getExpectedResponse(code):
            data["STATUS"] = self.getExpectedResponse(code)
          else:
            data["STATUS"] = self.getCode("OK")
        else:
          data["STATUS"] = self.getCode("OK")
    else:
      data = {"PROTOCOL":self.name.upper(), 
              "STATUS":self.getCode("OK"),
              "MESSAGE":data
              }

    return data


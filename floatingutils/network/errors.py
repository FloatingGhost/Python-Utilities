#!/usr/bin/env python3

class HFTPError(Exception):
  pass

hftp_codes = {
  #Status codes
  "OK":0,
  "FAIL":1,

  #Errors
  "FILE_NOT_FOUND":100,
  "ACCESS_DENIED":110,

  #Other codes
  "ALREADY_AUTHORIZED":200,
}


def code(words:str):
  return hftp_codes[words]

def error_name(code:int):
  r= (key for key,value in hftp_codes.items() if value==code)
  r = [i for i in r][0]
  return r

def errorDesc(code):
  code = int(code)
  return "Error {}: {}".format(code, error_name(code))

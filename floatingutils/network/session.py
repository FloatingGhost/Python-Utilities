
#!/usr/bin/env python3

from floatingutils.log import Log
from floatingutils.network.encryption import *

import random
import string

log = Log()



def genSessionKey():
  key = ""
  for i in range(20):
    key += random.choice(string.ascii_letters)
  return key


class Session:
  """Session object - keeps track of stuff I guess?"""

  def __init__(self, sessionKey):
    self.sessionKey = sessionKey
    self.authState = 0
    self.authCheck = 0

  def getSessionKey(self):
    return self.sessionKey

  def getAuthState(self):
    return self.authState

  def getCheck(self):
    return self.authCheck

  def setCheck(self, i):
    self.authCheck = i

  def setAuthState(self, i):
    self.authState = i

class SecureSession(Session):
  """Extends Session - Incorporates RSA key"""
 
  def __init__(self, rsa_public, sessionKey):
    self.rsa_public = rsa_public
    self.sessionKey = sessionKey 
    self.authState = 0
    self.authCheck = 0

  def getPublic(self):
    return self.rsa_public

class SessionManager:
  def __init__(self):
    self.sessions = {}

  def getSession(self, key):
    if key in self.sessions:
      return self.sessions[key]
    else:
      log.warning("Session {} could not be found!".format(key))
      return     

  def newSession(self, secure:bool, rsa_key:str):
    if secure and not rsa_key:
      log.error("Can't create a new SecureSession without an RSA Key!")
      return 
    
    new_key = genSessionKey()

    if secure:
      self.sessions[new_key] = SecureSession(rsa_key, new_key)
    else:
      self.sessions[new_key] = Session(new_key)

    return self.sessions[new_key]

  def endSession(self, key):
    """Entirely end a session"""

    del self.sessions[key]

  def getRSA(self, session_key):
    """Retrieve the RSA public key of a session"""

    s = self.getSession(session_key)
    if isinstance(s, SecureSession):
      return s.getPublicKey()    
    else:
      log.error("Session {} is not a SecureSession!".format(session_key))
      return


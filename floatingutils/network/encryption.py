#!/usr/bin/env python3

import rsa
from rsa.bigfile import *
import os
from binascii import hexlify, unhexlify
from floatingutils.log import Log

log = Log()

class LocalKeys:
  def __init__(self, keydir:str=os.path.expanduser("~/.hftp")):
    self.keydir = keydir
    self.loadKeys()

    print(self.PUBLIC_KEY.save_pkcs1())

  def loadKeys(self):
    try:
      log.info("Loading keys from {}".format(self.keydir))
      if not os.path.exists(self.keydir):
        log.info("{} does not exist. Creating...".format(self.keydir))
        os.mkdir(self.keydir)
        raise FileNotFoundError
      with open("{}/private.pem".format(self.keydir), "r") as f:
        self.PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(f.read())
      with open("{}/public.pem".format(self.keydir), "r") as f:
        self.PUBLIC_KEY = rsa.PublicKey.load_pkcs1(f.read())
    except FileNotFoundError as e:
      log.info("Could not find one of your keys -- {}".format(e))
      log.info("Generating keys...")
      self.PUBLIC_KEY,self.PRIVATE_KEY = rsa.newkeys(512)
      log.info("Saving keys to {}".format(self.keydir))

      with open("{}/private.pem".format(self.keydir), "w") as f:
        f.write(str(PRIVATE_KEY.save_pkcs1(), 'utf-8'))
      with open("{}/public.pem".format(self.keydir), "w") as f:
        f.write(str(PUBLIC_KEY.save_pkcs1(), 'utf-8'))


  def getPublic(self):
    return self.PUBLIC_KEY

  def getNetworkPublic(self):
    return str(self.PUBLIC_KEY.save_pkcs1(), 'utf-8')

  def encrypt(self, msg:str, other_public):
    try:
      return rsa.encrypt(bytes(msg, 'utf-8'), rsa.PublicKey.load_pkcs1(other_public))
    except rsa.pkcs1.CryptoError as e:
      log.error("Encryption could not finish")
      log.error(e)

  
  def decrypt(self, msg):
    try:
      return rsa.decrypt(bytes(msg, 'utf-8'), self.PRIVATE_KEY)      
    except rsa.pkcs1.DecryptionError as e:
      log.error("Could not decrypt!")

  def networkEncrypt(self, msg:str, other_public):
    msg = self.encrypt(msg, other_public)
    h =  hexlify(msg)
    assert(unhexlify(h))
    return h

  def networkDecrypt(self, msg):
    if msg[:2] == "b'":
      msg = msg[2:-1]
    msg = str(rsa.decrypt(unhexlify(msg), self.PRIVATE_KEY))
    if msg[:2] == "b'":
      msg = msg[2:-1]

    return (msg)

  def encryptFile(self, filename, other_public, netrep:bool=False):
    with open(filename, "rb") as i, open("tmp", "wb") as o:
      encrypt_bigfile(i, o, rsa.PublicKey.load_pkcs1(other_public))

    with open("tmp", "rb") as f:
      data = f.read()

    if netrep:
      data = hexlify(data) 
    return data

  def decryptFile(self, data, outfile, fromnetrep:bool=False):
    if fromnetrep:
      data = unhexlify(data)
    
    with open("tmp", "wb") as f:
      f.write(data)

    with open("tmp", "rb") as i, open(outfile, "wb") as o:
      decrypt_bigfile(i, o, self.PRIVATE_KEY) 
          

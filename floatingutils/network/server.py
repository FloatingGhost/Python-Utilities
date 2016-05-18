#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import cgi
import random
import os

from floatingutils.network.session import *
from floatingutils.log import Log
from floatingutils.network.encryption import *
from floatingutils.network.errors import *

log = Log()

rand = random.Random()

sman = SessionManager()

keys = LocalKeys(os.path.expanduser("~/.hftpd"))

auth = ""

with open(os.path.expanduser("~/.hftpd") + "/authorized_keys", "r") as f:
  auth = f.read()
  
pathways = {}

class Server(BaseHTTPRequestHandler):
  """Server Class -- A wrapper around BaseHTTPRequestHandler for less verbose use""" 
 
  def do_GET(self):
    self.send_response(200)
    self.send_header("content-type", "text/html")
    self.end_headers()
    self.wfile.write(
      bytes("<marquee><h1>Fek off post only no gets go away</h1></marquee>", "utf-8")
    )

    self.wfile.write(bytes("<marquee><input>Memes</input></marquee>", "utf-8"))
  def do_POST(self):
    log.info("Processing POST Req from {}".format(self.client_address))

    #Process all of the POST values into a nice little form
    form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
    
    #Dict-ify them for easy access
    post = {}
    for i in form.keys():
      post[i] = form.getvalue(i)
   
    msg = ""
    if self.path == "/auth":
      #Authenticate
      msg = (self.authenticate(post))
      
    else:
      if self.path in pathways:
        msg = pathways[self.path](sman.getSession(post["SESSION_KEY"]), post)
      else:
        msg = (self.post(post))
  
    if isinstance(msg, dict):
      self.do_SEND_DICT(msg)
    
    else:
      self.do_SEND(msg)

  def authenticate(self, post):
    """Authentication
       Process:
        C->S GET /auth <RSA>
        S->C ACK <S Key> Enc<i> -- C to STATE 1
        C->S GET /auth <S Key> Enc<i+i> Enc<j>
        S->C ACK Enc<j+1> -- C to STATE 2 (AUTH SUCCESS)
    """

    try:
      assert("SESSION_KEY" in post)
      s = sman.getSession(post["SESSION_KEY"])

      auth = s.getAuthState()

      if auth == 0:
        #Step one - Check the client's ident
        assert(post["REQUEST"] == "AUTH_CONFIRM")
        assert(post["CHALLENGE_ANSWER"])
        assert(post["AUTH_CHALLENGE"])
        log.info("Authorization Request from {}".format(self.client_address))
        check = keys.networkDecrypt(post["CHALLENGE_ANSWER"])
        check_exp = sman.getSession(post["SESSION_KEY"]).getCheck()+1
        log.info("Got {}, expected {}".format(check, check_exp))
        if (int(check) == int(check_exp)):
          log.info("{} Succesfully authenticated itself".format(self.client_address))
          ##Check succesfully completed
          sman.getSession(post["SESSION_KEY"]).setAuthState(1)
          ##It should have asked us for an auth
          s_check = int(keys.networkDecrypt(post["AUTH_CHALLENGE"]))
          conf = keys.networkEncrypt(str(s_check+1),
                                    sman.getSession(post["SESSION_KEY"]).getPublic()
                                    )
          return {"STATUS":code("OK"), "ACK":"SERV_IDENT", "CHALLENGE_ANSWER":conf}
        else:
          log.warning("{} Failed authentication checks!".format(self.client_address))
          return {"STATUS":code("FAIL"), "CODE":code("ACCESS_DENIED")}

      if auth == 1:
        return {"STATUS":code("FAIL"), "CODE":code("ALREADY_AUTHORIZED")}

    except AssertionError:
      assert("RSA_KEY" in post)
      with open(os.path.expanduser("~/.hftpd/authorized_keys"),"r") as f:
        g = f.read()
        log.info("Checking that {}\n is in \n {}".format(post["RSA_KEY"], g))
        if not (post["RSA_KEY"] in g):
          return {"STATUS":code("FAIL"), "CODE":code("ACCESS_DENIED")}
      #New user
      s = sman.newSession(True, post["RSA_KEY"])
      s.setCheck(rand.randint(1, 1000000))
      enc = keys.networkEncrypt(str(s.getCheck()), s.getPublic())
      return {"ACK": "HELLO_FRIEND", "RSA_PUBLIC":keys.getNetworkPublic(), 
              "SESSION_KEY":s.getSessionKey(), 
              "AUTH_CHALLENGE":enc
             }      
    
  def post(postvals : dict):
    log.info("Placeholder POST function -- Assign with Server.addPost()")
  
  def addPost(self, function):
    self.post = function

  def do_SEND(self, msg:str, resp:int=200, content:str="text/plain"):
    self.send_response(resp)

    self.send_header("content-type", content)

    self.end_headers()

    log.info("Responding {}".format(msg))
    self.wfile.write(bytes(msg, 'utf-8'))
    log.info("Sent.")

  def do_SEND_DICT(self, msg:dict, resp:int=200, content:str="text/plain",
                         field_sep:str = "//////"):
    """Send a dictionary of field-values over the network"""
    self.send_response(resp)
  
    self.send_header("content-type", content)

    self.end_headers()

    for i in msg:
      self.wfile.write(bytes("{}\n{}\n{}\n".format(i, msg[i], field_sep), 'utf-8'))

def serverMainLoop(server, ip="localhost", port=9000):
  try:
    log.info("Starting server on {}:{}".format(ip, port))

    s = HTTPServer((ip, port), server)

    s.serve_forever()
  except KeyboardInterrupt:
    log.info("Shutting down...")
    s.socket.close()

def addPathway(path, func):
  if path not in pathways:
    log.info("Added pathway for {}".format(path))
    pathways[path] = func
    return
  log.error("Could not add pathway {}".format(path))


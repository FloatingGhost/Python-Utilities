#!/usr/bin/env python3

from Skype import *
import os
from Reddit import *
from AI import *
import sys

c = Chat(cmd="~", botname="Fuego is a meme")


c.addTrigger("test", "yes this works")
c.addTrigger("cis", "CISGENDERED WHITE MALE")
c.addTrigger("meme", "Nice meme!")
c.addTrigger("bot", "I'm not here", True)
def quit():
  sys.exit(0)  

def add(x, y):
  print("Running with {} and {}".format(x,y))
  try:  
    c.send(str(float(x)+float(y)))
  except:
    try:
      c.send(str(x+y))
    except:
      c.send("Pls give 2 of the same type :c")

def addTrigger(a, b):
  print("Adding trigger {} with {}".format(a,b))
  c.addTrigger(a,b)

def run(a):
  print("OS {}".format(a))
  os.system(a+"&")


model = None

def trainReddit(subname):
  global model
  r = Reddit()
  print("Training for {}".format(subname))
  model = NGram(r.getSubTitles(subname), 2)
  c.send("Trained")
  
def gen(a):
  q = ""
  for i in range(int(a)):
        q += model.generate() + "\n"
  c.send(q)

c.addCommand("add", "Add two numbers", "add x y", add, ["x", "y"])
c.addCommand("trig", "Add a trigger", "trig x y", addTrigger, ["t", "tr"])
c.addCommand("reddit", "Train on reddit", "Train [sub]", trainReddit, ["sub"])
c.addCommand("gen", "Generate messages", "gen n", gen, ["n"])
c.addCommand("quit", "quit","quit", quit)
c.mainloop()

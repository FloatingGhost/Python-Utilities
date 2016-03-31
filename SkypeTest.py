#!/usr/bin/env python3

from Skype import *
import os
from Reddit import *
from AI import *
import sys
from Chan import *
import pickle

c = Chat(cmd="~", botname="Memebot 2k16")


c.addTrigger("test", "yes this works")
c.addTrigger("cis", "CISGENDERED WHITE MALE")
c.addTrigger("meme", "Nice meme!")
c.addTrigger("bot", "I'm not here", True)
def quit(memes):
  c.send("Bot shutting down")
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
  c.send("Training for r/{}".format(subname))
  model = NGram(r.getSubTitles(subname), 2)
  c.send("Trained")
 
def trainRedditComments(subname):
  global model
  r = Reddit()
  c.send("Training on the comments of r/{}".format(subname))
  model = NGram(r.getComments(subname),2)
  c.send("Trained")

def trainSelf(subname):
  global model
  r = Reddit()
  c.send("Training on the self text of r/{}".format(subname))
  model = NGram(r.getOPs(subname),2)
  c.send("Trained")

 
def trainChan(board):
  global model
  try:
    ch = FourChan(board)
    print(ch)
    c.send("Training for /{}/ ({})\nThis Could take a while".format(board,ch.board.title))
    model = NGram(ch.getTitles(),2)
    c.send("Trained")
  except:
    c.send("Could not train - check board name")
def gen(a):
  q = ""
  for i in range(int(a)):
        q += model.generate() + "\n"
  c.send(q)

def save(name):
  global model
  os.mkdir("models")
  try:
    with open("models/{}.sav".format(name), "wb") as f:
      pickle.dump(model,f)
    c.send("Saved {}".format(name))
  except Exception as ex:
    c.send("Failed with {}".format(ex))

def load(name):
  global model
  try:
    with open("models/{}.sav".format(name), "rb") as f:
      model = pickle.load(f)
    c.send("Loaded {}".format(name))
  except Exception as ex:
    c.send("Failed with {}".format(ex))

c.addCommand("add", "Add two numbers", "add x y", add, ["x", "y"])
c.addCommand("trig", "Add a trigger", "trig x y", addTrigger, ["t", "tr"])
c.addCommand("reddit", "Train on reddit", "Train [sub]", trainReddit, ["sub"])
c.addCommand("redditcom", "", "", trainRedditComments, ["sub"])
c.addCommand("redditself", "", "", trainSelf, ["sub"])
c.addCommand("gen", "Generate messages", "gen n", gen, ["n"])
c.addCommand("quit", "quit","quit", quit, ["yes"])
c.addCommand("chan", "chan", "chan", trainChan, ["board"])
c.addCommand("save", "", "", save, ["name"])
c.addCommand("load", "", "", load, ["name"])
c.mainloop()

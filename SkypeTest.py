#!/usr/bin/env python3

from Skype import *

c = Chat(cmd="~", botname="May is a meme")


c.addTrigger("test", "yes this works")

def x(meme):
  c.send("test function, arg val was {}".format(meme))

def y(meme):
  c.send(meme.upper())

c.cmdProc.addCommand("test", "", "", x, ["meme"])
c.cmdProc.addCommand("upper", "", "", y, ["meme"])
c.mainloop()

#!/usr/bin/env python3

###Test file for command processor
from nose.tools import nottest
from commandprocessor import *
import atexit
import time
from log import Log
c = CommandProcessor(debug=True)
log = Log()
c.start()
time.sleep(1)
@nottest
def return_1():
  return 1

@nottest
def return_arg(a: int):
  return a

@nottest 
def return_optarg(a:int=5):
  return a

@nottest
def return_nocheck(a=5):
  return a

@nottest
def return_argPlusOpt(a: int, b:int=5):
  c = a+b
  return  c

def test_add_command():
  c.addCommand("ret1", return_1)
  c.addCommand("reta", return_arg)
  c.addCommand("reto", return_optarg)
  c.addCommand("retadd", return_argPlusOpt)
  c.addCommand("retonocheck", return_nocheck)
def test_run_command():
  c.push("!ret1")
  c.push("!reta 5")
  c.push("!reto")
  c.push("!reto a")
  c.push("!retadd 5")
  c.push("!retadd 1,2")
  c.push("!retonocheck")
  c.push("!retonocheck hello")
  assert(1 == c.getOutput())
  assert(5 == c.getOutput())
  assert(5 == c.getOutput())
  assert("Error" in c.getOutput())
  assert(10 == c.getOutput())
  assert(3 == c.getOutput())
  assert(5 == c.getOutput())
  assert("hello" == c.getOutput())
c.exit()

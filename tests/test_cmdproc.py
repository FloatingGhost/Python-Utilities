#!/usr/bin/env python3

###Test file for command processor
from nose.tools import nottest
from commandprocessor import *
import atexit
import time
from log import Log
c = CommandProcessor(module_path="testmods", debug=False)
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

@nottest
def adminstuff():
  admin = 1

def test_add_command():
  c.addCommand("ret1", return_1)
  c.addCommand("reta", return_arg)
  c.addCommand("reto", return_optarg)
  c.addCommand("retadd", return_argPlusOpt)
  c.addCommand("retonocheck", return_nocheck)
  c.addCommand("adminstuff", adminstuff)

def test_run_command():
  c.push("!ret1")
  c.push("!reta 5")
  c.push("!reto")
  c.push("!reto a")
  c.push("!retadd 5")
  c.push("!retadd 1,2")
  c.push("!retonocheck")
  c.push("!retonocheck hello")
  assert(1 == c.getOutput()[0])
  assert(5 == c.getOutput()[0])
  assert(5 == c.getOutput()[0])
  assert("Error" in c.getOutput()[0])
  assert(10 == c.getOutput()[0])
  assert(3 == c.getOutput()[0])
  assert(5 == c.getOutput()[0])
  assert("hello" == c.getOutput()[0])
def test_load():
  c.loadModule("import_test")
  c.push("!lsmod")
  log.info(c.getOutput()[0])
  c.push("!help imported_func")
  log.info(c.getOutput()[0])
def test_quit():
  c.push("!quit")

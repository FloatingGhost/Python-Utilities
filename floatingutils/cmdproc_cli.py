#!/usr/bin/env python3 

from commandprocessor import CommandProcessor

cmd = CommandProcessor("cmdcli.conf")
cmd.start()
cmd.setCallback(print)

i = ""
  
while i != "!quit":
  i = input("CmdProc :: ")
  cmd.push(i)
  

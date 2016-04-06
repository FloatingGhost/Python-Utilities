#!/usr/bin/env python3

def toBool(i):
  if not type(i) == type("string"):
    return
  i = i.lower()
  if "y" in i:
    return True
  return False

def fromBool(i):
  if i:
    return "Yes"
  return "No"

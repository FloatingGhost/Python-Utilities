#!/usr/bin/env python3

import glob
from log import Log

log = Log()

def notthere(string, l):
  for i in l:
    if string in i:
      return False
  return True

log.info("Getting all python files...")
f = glob.glob("*.py")

name = input("Author Name: ")

if input("Add Package? (y/n) ") == "y":
  package = input("Package Name: ")
else:
  package = None

for i in f:
  log.info("Writing changes to {}...".format(i))
  with open(i, 'r') as g:
    lines = g.readlines()
    if "#!" not in lines[0]:
      lines.insert(0, "#!/usr/bin/env python\n")
    if notthere("__author__",lines):
      lines.insert(1, "__author__ = '{}'\n".format(name))
    if package:
      if notthere("__package__", lines):
        lines.insert(2, "__package__ = '{}'\n\n".format(package))
  with open(i, 'w') as g:
    g.writelines(lines)  

log.info("Done.")    

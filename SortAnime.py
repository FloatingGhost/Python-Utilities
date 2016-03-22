#!/usr/bin/env python3

import re
import glob
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Sort a media folder out")

parser.add_argument("format", help="The file format to sort")

parser.add_argument("--exec", action="store_true", default=False,
                    help="Run the sorting script")

args = parser.parse_args()

if args.exec:
  print("This will actually edit your files. Is this ok?")
  if not (input("[y/N] ").lower() == "y"):
    print("Ok, exiting.")
    sys.exit()


reg=  "\[[A-Za-z0-9]*\] [A-Za-z -]* - [0-9][0-9]? \[[A-Zp0-9]*\]\.{}".format(
                                                                args.format
                                                                       )
reg = re.compile(reg)

files = glob.glob("*.{}".format(args.format))

print("="*30)
print("Commands to run")
print("="*30)

for f in files:
  if reg.match(f):
    subgroup,sep,f1 = f.partition("] ")
    subgroup = subgroup[1:]
    series,sep,f2 = f1.partition(" - ")
    episode,sep,f3 = f2.partition(" [")
    d = "Anime/{}".format(series.replace(" ", "-"))
    try:
      os.mkdir(d)
    except:
      pass
    cmd = "mv '{}' {}".format(f, d)
    print(cmd)
    if args.exec:
      os.system(cmd)

print("="*30)
if not args.exec:
  print("Add --exec to your arguments if you wish to run this")    

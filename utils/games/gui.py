#!/usr/bin/env python3

import curses
from log import Log
import os
import atexit

log = Log()

class GUI:
  def __init__(self):
    log.info("Starting GUI...")
    self.screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    self.screen.keypad(True)
    self.windows = []
    atexit.register(self.close)
    log.info("GUI started and ready.")

  def close(self):
    log.info("Stopping GUI.")
    curses.nocbreak()
    curses.echo()
    self.screen.keypad(False)
    curses.endwin()
    log.info("GUI Stopped.")
    os.system("reset")

  def addWindow(self, x, y, width, height):
    log.info("Adding GUI window at {}, {} to {}, {}".format(x,y,x+width,y+height))
    self.winows.append(curses.newwin(height, width, y, x))
    log.info("Window added succesfully.")

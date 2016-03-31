#!/usr/bin/env python

import basc_py4chan as chan

class Chan:
  def __init__(self, board):
    self.board = chan.Board(board)
    print(self.board)

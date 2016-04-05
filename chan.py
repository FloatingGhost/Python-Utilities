#!/usr/bin/env python

import basc_py4chan as chan
import re
from log import Log

class FourChan:
  """Wrapper class to py4chan - 4chan API"""

  def __init__(self, board):
    self.log = Log()
    self.log.info("Getting /{}/...".format(board))  
    try:
      self.board = chan.Board(board)
      self.log.info("/{}/ was fetched succesfully".format(board))
    except Exception as e:
      self.log.error("Failed to fetch /{}/ -- {}".format(board, e))

  def getPosts(self,limit=10):
    self.log.info("Getting posts - limit of {}".format(limit))
    return self.board.get_all_thread_ids()[:limit+1]

  def getTitles(self):
    self.log.info("Getting thread titles...")
    q = []
    for x in self.getPosts():
      b = self.board.get_thread(x).posts
      q += [self._scrub(y.comment) for y in b]
    self.log.info("Got titles of threads succesfully")
    return [x for x in q if x != '']

  def _scrub(self, post):
    """Clean up the posts, remove all HTML and formatting"""
    scrubs = ["<span class=\"quote\">", "<br>", "</span>","</s>"]
    
    for i in scrubs:
      post = post.replace(i, " ")
    post = post.replace("&gt;", ">").replace("&#039;", "'").replace("&quot;", "\"")
    q = re.compile("</[ab]>|<span [A-Za-z0-9\#\"\ \:\=]*> *</?b>|com\/post\/[0-9]*|<a href=\"https\:\/\/boards|>>[0-9]*<\/a>|<a [\ \/a-z\=\"\#0-9]*>>>[0-9]*<\/a>|<a [\ \/a-z\=\"\#0-9]*>")
    for w in q.findall(post):
      post = post.replace(w, " ")
    return post

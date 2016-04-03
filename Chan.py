#!/usr/bin/env python

import basc_py4chan as chan
import re

class FourChan:
  def __init__(self, board):
    print("Training!")
    self.board = chan.Board(board)

  def getPosts(self,limit=10):
    return self.board.get_all_thread_ids()[:limit+1]

  def getTitles(self):
    print("Getting titles!")
    q = []
    for x in self.getPosts():
      b = self.board.get_thread(x).posts
      q += [self.scrub(y.comment) for y in b]
    print("Got posts")
    return [x for x in q if x != '']

  def scrub(self, post):
    scrubs = ["<span class=\"quote\">", "<br>", "</span>","</s>"]
    
    for i in scrubs:
      post = post.replace(i, " ")
    post = post.replace("&gt;", ">").replace("&#039;", "'").replace("&quot;", "\"")
    q = re.compile("</[ab]>|<span [A-Za-z0-9\#\"\ \:\=]*> *</?b>|com\/post\/[0-9]*|<a href=\"https\:\/\/boards|>>[0-9]*<\/a>|<a [\ \/a-z\=\"\#0-9]*>>>[0-9]*<\/a>|<a [\ \/a-z\=\"\#0-9]*>")
    for w in q.findall(post):
      post = post.replace(w, " ")
    return post

if __name__ == "__main__":
    c = Chan("g")
    print(c.getTitles())

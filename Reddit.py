#!/usr/bin/env python3

import praw

class Reddit:
  def __init__(self, useragent="FloatingGhost's python utility"):
    self.api = praw.Reddit(user_agent=useragent)
    
  def getSub(self, subname, limit=100):
    return self.api.get_subreddit(subname).get_hot(limit=limit)

  def getOPs(self, subname, limit=20):
    x = self.getSub(subname, limit)
    return [y.selftext for y in x if y.selftext != '']

  def getSubTitles(self, subname, limit=500):
    return [str(x).split("::")[-1][1:] for x in self.getSub(subname, limit)]

  def getComments(self, subname, limit=500):
    x = self.api.get_subreddit(subname).get_comments(limit=limit)
    return [y.body for y in x]

#!/usr/bin/env python3

import praw
from log import Log

class Reddit:
  def __init__(self, useragent="FloatingGhost's python utility"):
    self.log = Log()
    self.log.info("Connecting to reddit...")
    self.api = praw.Reddit(user_agent=useragent)
    self.log.info("Connected.")

  def getSub(self, subname, limit=100):
    """Get a subreddit"""

    self.log.info("Retrieving r/{}".format(subname))
    return self.api.get_subreddit(subname).get_hot(limit=limit)

  def getOPs(self, subname, limit=20):
    """Get the self text of the OPs in a subreddit"""

    self.log.info("Getting the OP selftext in {} (limit {})".format(subname,limit))
    x = self.getSub(subname, limit)
    return [y.selftext for y in x if y.selftext != '']

  def getSubTitles(self, subname, limit=500):
    """Get the titles of a subreddit's posts"""
  
    self.log.info("Getting the titles in r/{}".format(subname))
    return [str(x).split("::")[-1][1:] for x in self.getSub(subname, limit)]

  def getComments(self, subname, limit=500):
    """Get the comments of a subreddit"""
    
    self.log.info("Getting the comments of r/{}".format(subname))
    x = self.api.get_subreddit(subname).get_comments(limit=limit)
    return [y.body for y in x]

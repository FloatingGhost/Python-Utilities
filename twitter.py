#!/usr/bin/env python3

import tweepy
import re

class Twitter:
  def __init__(self):
    [keys redacted]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    self.api = tweepy.API(auth)

    self.mention = re.compile("@[A-Z\:a-z0-9\_]*|RT|#[A-Za-z0-9_]*|http://[A-Za-z0-9\._\:\/]*|https://[A-Za-z0-9\._\:\/]*")

  def getUser(self, username):
    return self.api.get_user(username)

  def getTweets(self, username, limit=200):
    return [self.scrub(x.text) for x in self.api.user_timeline(username, count=limit)]

  def scrub(self, text):
    for i in self.mention.findall(text):
      text = text.replace(i, "")
    return text.replace("&gt;", ">").strip()


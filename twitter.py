#!/usr/bin/env python3

import tweepy
import re

class Twitter:
  def __init__(self):
    consumer_key = "O2oCD1Uop8yL8Noidvhvnwb7i"
    consumer_secret = "DRHWCKmb9Ae3ZZr7H6MAkmCyJxbThRxrujWqVnB119Vbw7ukEw"

    access_token = "88449821-dzVb1b22HKS0zetoU8nnmkVYfuNxjW3Lnx4BG97L5"
    access_token_secret = "QmqcKU80AqLVfnivg0APMPAl4h0taBQjLgpmPPERajJf0"

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


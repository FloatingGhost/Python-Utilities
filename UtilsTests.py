#!/usr/bin/env python3

import unittest
from conf import Conf
from AI import *

class TestConfig(unittest.TestCase):

  def setUp(self):
    self.c = Conf("testconfig.conf")
  def test_read(self):
    self.assertEqual("test", self.c.get("test"))
    self.assertEqual(":test setting", self.c.get("b"))
    self.assertEqual("",self.c.get("2"))
    self.assertEqual(0, self.c.get(""))
    self.assertEqual(0, self.c.get("memes"))

  def test_set(self):
    self.assertTrue(self.c.set("memes", "lel"))
    self.assertEqual("lel", self.c.get("memes"))
    self.assertFalse(self.c.set("", "hello"))

class TestAI(unittest.TestCase):
  def setUp(self):
    self.corpus = "the cat sat on the mat, the cat ran"

  def test_bigram(self):
    model = NGram(self.corpus, 2)
    self.assertEqual(0.5, model.getProb("sat", "cat"), True)    

  def test_trigram(self):
    model = NGram(self.corpus, 3)
    self.assertEqual(0.5, model.getProb("ran", "the cat"))
if __name__ == '__main__':
    unittest.main()

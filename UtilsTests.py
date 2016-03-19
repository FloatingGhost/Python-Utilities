#!/usr/bin/env python3

import unittest
from conf import Conf
from AI import *

class TestConfig(unittest.TestCase):

  def setUp(self):
    self.c = Conf("testconfig.conf")
  def test_read(self):
    self.assertEqual("test", self.c.getValue("test"))
    self.assertEqual(":test setting", self.c.getValue("b"))
    self.assertEqual(0,self.c.getValue("2"))
    self.assertEqual(0, self.c.getValue(""))
    self.assertEqual(0, self.c.getValue("memes"))

  def test_set(self):
    self.assertTrue(self.c.setValue("memes", "lel"))
    self.assertEqual("lel", self.c.getValue("memes"))
    self.assertFalse(self.c.setValue("", "hello"))
  
  def test_write(self):
    self.assertTrue(self.c.setValue("memes", "lel"))
    self.c.writeFile('newtestconf.conf')

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

#!/usr/bin/env python3

import unittest
from conf import Conf
from AI import *
from CommandProcessor import CommandProcessor

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

def testdef(val):
  return val

class TestCommandProcessor(unittest.TestCase):
  def setUp(self):
    self.proc = CommandProcessor()

  def test_addcmd(self):
    self.assertEqual(1, self.proc.addCommand("test", "A test cmd", "No Usage"))
    self.proc.addArgument("test", "name", "No help")

  def test_gethelp(self):
    self.assertEqual(1, self.proc.addCommand("test", "A test cmd", "No Usage"))
    self.assertNotEqual([], self.proc.getAllHelp())

  def test_runcmd(self):
    self.assertEqual(
      self.proc.addCommand("def", "", "", testdef, ["testarg"]),
      1
    )
    self.assertEqual("memes", self.proc.processCommand("def memes"))


if __name__ == '__main__':
    unittest.main(verbosity=2)

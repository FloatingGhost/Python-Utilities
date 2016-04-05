#!/usr/bin/env python3

import unittest
from conf import Conf,YamlConf
from aiutils import *
from commandprocessor import CommandProcessor
from reddit import *

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

class TestYAMLConf(unittest.TestCase):
  def setUp(self):
    self.c = YamlConf("YamlConfig.conf")

  def test_getvalue(self):
    self.assertEqual(3,self.c.getValue("magic", "c", "d"))
    self.assertEqual(1,self.c.getValue("test", "a"))

  def test_getnonexistantvalue(self):
    self.assertIsNone(self.c.getValue("hello"))

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
  yield val

class TestCommandProcessor(unittest.TestCase):
  def setUp(self):
    self.proc = CommandProcessor(debug=True)

  def test_addcmd(self):
    self.assertEqual(1, self.proc.addCommand("test", "A test cmd", print, "No Usage"))
    self.proc.addArgument("test", "name", "No help")

  def test_gethelp(self):
    self.assertEqual(1, self.proc.addCommand("test", "A test cmd", "No Usage"))
    self.assertNotEqual([], self.proc.getAllHelp())

  def test_runcmd(self):
    self.assertEqual(
      self.proc.addCommand("def", "", "", testdef, ["testarg"]),
      1
    )
    print([x for x in self.proc.processCommand("!def memes")])
    self.assertEqual("memes", next(self.proc.processCommand("!def memes")))
  
  def test_loadmodule(self):
    self.assertTrue(next(self.proc.loadModule("testmodule")))
    print(next(self.proc.processCommand("!a")))
    self.assertEqual(1, next(self.proc.processCommand("!a")))

  def test_unloadmodule(self):
    self.assertTrue(next(self.proc.loadModule("testmodule")))
    self.assertEqual(1, next(self.proc.processCommand("!a")))
    self.assertTrue(next(self.proc.unloadModule("testmodule")))
    self.assertEqual("Command not found", next(self.proc.processCommand("!a")))
class TestReddit(unittest.TestCase):
  def setUp(self):
    self.r = Reddit()

  def test_getsub(self):
    self.assertIsNotNone(self.r.getSub("funny"))



if __name__ == '__main__':
    unittest.main(verbosity=2)

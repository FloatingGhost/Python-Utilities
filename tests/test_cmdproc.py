from commandprocessor import CommandProcessor as cmd
from nose.tools import nottest

proc = cmd(debug=True)

@nottest
def no_args():
  return 1

@nottest
def one_arg(a):
  return a

@nottest
def two_args(a,b):
  return a+b


def test_addcommand():
  assert ( proc.addCommand("test_noargs",
                           "A test command with 0 arguments",
                           "test_noargs",
                           no_args
                           )
         )

  assert ( proc.addCommand("test_onearg",  
                           "A test command that returns its arg",
                           "test_onearg",
                           one_arg,
                           ["argument"]
                          )
          )

  assert( proc.addCommand("test_twoarg",
                          "A test that adds its 2 args",
                          "test_twoarg",
                          two_args,
                          ["first", "second"]
                         )
        )

def test_runcommand():
  #No args
  assert ( 1 == next(proc.processCommand("!test_noargs" )))
  assert ( "1" == next(proc.processCommand("!test_onearg 1")))
  assert ("hello world" == next(proc.processCommand(
                  "!test_twoarg hello, world")))
  
def test_loadmodule():
  next(proc.loadModule("testmods.import_test"))
  assert ( 1 == next(proc.processCommand("!imported_func")) )

def test_unloadmodule():
  next(proc.unloadModule("testmods.import_test"))
  assert ( "Command not found" == next(proc.processCommand(
                                          "!imported_func")))


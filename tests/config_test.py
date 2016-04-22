import nose

from floatingutils.conf import Conf

c = Conf("test_configs/basic_config.conf")

def test_read():
  assert( c.getValue("value") == "Success" )
  assert( c.getValue("other_value") == "Another success" )
  assert( c.getValue("faliure") == 0 )
  
def test_set():
  assert( c.setValue("test_set", "One more success") )
  assert( c.getValue("test_set") == "One more success" )



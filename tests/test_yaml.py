from floatingutils.conf import YamlConf

##setup
c = YamlConf("test_configs/yaml_config.conf")

def test_getkey():
  assert ( c.getValue("key") == "value" )
  assert ( c.getValue("boolean") == True )
  assert ( c.getValue("number") == 1)
  assert ( c.getValue("dict") == {"key":"value",
                                  "boolean": True,
                                  "number": 1})

def test_getsubkey():
  assert ( c.getValue("dict", "key") == "value" )
  assert ( c.getValue("dict", "boolean") == True )
  assert ( c.getValue("dict", "number") == 1 )

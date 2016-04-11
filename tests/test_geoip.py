from geoip import Geo

g = Geo()

def test_getme():
  assert ( g.get(g._my_ip())["country_code"] == "GB" )

#!/usr/bin/env python3

from log import Log
import json
from pygeoip import GeoIP
from conf import YamlConf


log = Log()
config = YamlConf("")


class Geo(GeoIP):
  def __init__(self, filename=None):
    if not filename:
      filename = config.getValue("geoip","database_path")
    GeoIP.__init__(filename)

  def get(self, ip_addr):
    return self.record_by_addr(ip_addr)

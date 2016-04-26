#!/usr/bin/env python3
__author__ = 'Hannah Ward'
__package__ = 'floatingutils'


from floatingutils.log import Log
import json
from pygeoip import GeoIP
from floatingutils.conf import YamlConf
from requests import get
import os

log = Log()
config = YamlConf(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config/geoip.conf"))


class Geo(GeoIP):
  def __init__(self, filename=None):
    if not filename:
      filename = config.getValue("geoip","database_path")
    GeoIP.__init__(self, filename)

  def get(self, ip_addr):
    log.debug(self.record_by_addr(ip_addr))
    return self.record_by_addr(ip_addr)

  def _my_ip(self):
    return get("https://api.ipify.org").text


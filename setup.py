#!/usr/bin/env python3

from distutils.core import setup

setup(name='FloatingUtils' ,
      version='0.1',
      description='Python Utilities',
      author='Hannah Ward',
      author_email='hannah.ward9001@gmail.com',
      url='',
      packages=['floatingutils'],
      data_files=[("./config", ['./floatingutils/config/geoip.conf', './floatingutils/config/logging.conf'])], 

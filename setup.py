#!/usr/bin/env python3

from distutils.core import setup

setup(name='FloatingUtils' ,
      version='0.1',
      description='Python Utilities',
      author='Hannah Ward',
      author_email='hannah.ward9001@gmail.com',
      url='',
      packages=['floatingutils', 'floatingutils.network',
                'floatingutils.ai', 'floatingutils.api'
                ],
      package_data={"floatingutils":['config/*.conf'],
                    "floatingutils.api":["config/*.conf"]},
    ) 

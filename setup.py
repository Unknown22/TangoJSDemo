#!/usr/bin/env python

import os
from setuptools import setup, find_packages

# Read function
def safe_read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""

# Setup
setup(name="tangojs-demo",
      version="0.1.1",
      description="Demo setup for TangoJS",
      license="GPLv3",
      long_description=safe_read("README.md"),
      include_package_data=True,
      packages=find_packages(),
      package_data={'tangojsdemo': ['images/*.png']},
      data_files=[('/usr/share/applications', ['tangojs-demo.desktop'])],
      entry_points={'console_scripts': ['runtangojsdemo = tangojsdemo:main' ]}
      )

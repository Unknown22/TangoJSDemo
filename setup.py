#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from sys import platform

# Read function
def safe_read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""

# install_requires
install_requires = ['wheel']

python_version = sys.version_info
if python_version >= (3,4):
    install_requires.append('setuptools==33.1.1')
else:
    # SystemExit
    sys.exit('! Exception ! \nIncorrect python version: %s' % python_version)

data_files = []
if platform == "linux" or platform == "linux2":
    data_files = [('/usr/share/applications',['tangojs-demo.desktop'])]

# Setup
setup(name="tangojs-demo",
      version="0.1.1",
      description="Demo setup for TangoJS",
      license="MIT",
      long_description=safe_read("README.md"),
      include_package_data=True,
      packages=find_packages(),
      package_data={'tangojsdemo': ['images/*.png']},
      data_files=list(data_files),
      entry_points={'console_scripts': ['runtangojsdemo = tangojsdemo:main' ]},
      install_requires=install_requires,
      )

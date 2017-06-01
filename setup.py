#!/usr/bin/env python

import os
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup

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
      license="MIT",
      long_description=safe_read("README.md"),
      include_package_data=True,
      packages=find_packages(),
      package_data={'tangojsdemo': ['images/*.png']},
      data_files=[('/usr/share/applications', ['tangojs-demo.desktop'])],
      zip_safe = True,
      entry_points={'console_scripts': ['runtangojsdemo = tangojsdemo:main' ]},
      extras_require={
         ':python_version <= "3.4"': [
                'setuptools==33.1.1'
      ]}
      )

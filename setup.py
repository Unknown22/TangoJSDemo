#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="tangojs-demo",
      version="0.1.1",
      description="Demo setup for TangoJS",
      license="GPLv3",
#      package_dir={'': 'tangojsdemo', },
      include_package_data=True,
      packages=find_packages(),
      package_data={'tangojsdemo': ['images/*.png']},
      data_files=[('/usr/share/applications', ['tangojs-demo.desktop'])],
      scripts=['script/runtangojsdemo']
      )

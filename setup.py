# -*- coding: utf-8 -*-

'''
Created on 18.5.2018
@author: Samuli Rahkonen
'''

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_file = f.read()

install_requires = []

setup(name='json_selector',
      version='0.0.1',
      description=readme,
      author='Samuli Rahkonen',
      install_requires=install_requires,
      packages=find_packages(),
      license=license_file
)
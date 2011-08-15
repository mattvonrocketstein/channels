#!/usr/bin/env python
""" setup.py for channels
"""
from setuptools import setup, find_packages
setup(
    name        ='channels',
    version     = '.1',
    description = 'backend-agnostic sugar for message passing',
    author      = 'mattvonrocketstein, in the gmails',
    url         = 'one of these days',
    package_dir = {'': 'lib'},
    packages    = find_packages('lib'),
    )

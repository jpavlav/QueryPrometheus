#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

# Thank you https://github.com/kennethreitz/setup.py
# May flesh this out to include the upload functionality.

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'prometheus'
DESCRIPTION = 'Query prometheus for data'
URL = 'https://github.com/jpavlav/QueryPrometheus'
EMAIL = 'jpavlav@gmail.com'
AUTHOR = 'Justin Palmer'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '0.1.0'
PACKAGES = ['prometheus']
REQUIRED = [
    'requests'
]

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except OSError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=PACKAGES,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: setup
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Setup script to use with pip for the project microanalysis_file_format.
"""

###############################################################################
# Copyright 2020 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Project modules.
from microanalysis_file_format import __author__, __email__, __version__, __project_name__

# Globals and constants variables.
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = []
    for line in requirements_file:
        line = line.strip()
        if len(line) > 0:
            requirements.append(line)


setup(name=__project_name__,
      version=__version__,
      url='https://github.com/drix00/microanalysis_file_format',
      project_urls={
          "Bug Tracker": "https://github.com/drix00/microanalysis_file_format/issues",
          "Documentation": "https://microanalysis_file_format.readthedocs.io/",
          "Source Code": "https://github.com/drix00/microanalysis_file_format",
      },
      description="Project to read and write various x-ray spectrum file format.",
      long_description=readme + '\n\n' + history,
      author=__author__,
      author_email=__email__,
      maintainer=__author__,
      maintainer_email=__email__,
      keywords="python science physics",
      license="Apache License, Version 2.0",
      license_file="LICENSE",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: Apache Software License',
                   'Natural Language :: English',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering',
                   ],
      packages=find_packages(),
      platforms='any',
      install_requires=requirements,
      zip_safe=False,
      include_package_data=False,  # Do not include test data
      test_suite='tests',
      tests_require=['pytest', 'coverage', 'pytest-cov'],
      extras_require={
          'testing': ['pytest', 'coverage', 'pytest-cov'],
          'develop': ['setuptools', 'Sphinx', 'sphinx-rtd-theme', 'pytest', 'coverage', 'pytest-cov']
      },
)

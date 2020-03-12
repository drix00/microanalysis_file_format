#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: __init__
   :synopsis: Init for the package.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Init for the package.
"""

###############################################################################
# Copyright 2007 Hendrix Demers
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
import os.path

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
__author__ = """Hendrix Demers"""
__email__ = 'hendrix.demers@mail.mcgill.ca'
__version__ = '0.1.0'


def get_current_module_path(module_path, relative_path=""):
    base_path = os.path.dirname(module_path)

    file_path = os.path.join(base_path, relative_path)
    file_path = os.path.normpath(file_path)

    return file_path


def is_test_data_file(file_path):
    good_test_data_file = True

    if not os.path.isfile(file_path):
        good_test_data_file = False
        return good_test_data_file

    with open(file_path, 'rt') as test_data_file:
        try:
            lines = test_data_file.readlines()

            if len(lines) == 3:
                if lines[0].strip() == "version https://git-lfs.github.com/spec/v1":
                    good_test_data_file = False
                if lines[1].startswith("oid"):
                    good_test_data_file = False
                if lines[2].startswith("size"):
                    good_test_data_file = False
        except UnicodeDecodeError:
            good_test_data_file = True

    return good_test_data_file

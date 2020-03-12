#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: pySpectrumFileFormat.test_init

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`pySpectrumFileFormat.__init__`.
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
from pySpectrumFileFormat import get_current_module_path, is_test_data_file

# Globals and constants variables.


def test_is_test_data_file(tmp_path):
    file_path = os.path.join(tmp_path, "lfs_test_file.txt")
    with open(file_path, 'w') as lfs_file:
        lines = """version https://git-lfs.github.com/spec/v1
oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393
size 12345

"""
        lfs_file.writelines(lines)

    assert is_test_data_file(file_path) is False

    assert is_test_data_file(get_current_module_path(__file__)) is False

    assert is_test_data_file(__file__) is True

    # self.fail("Test if the TestCase is working.")

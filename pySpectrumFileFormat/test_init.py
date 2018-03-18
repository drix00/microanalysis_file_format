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
import unittest
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.

# Project modules.
from pySpectrumFileFormat import get_current_module_path, is_test_data_file

# Globals and constants variables.


class TestInit(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.file_path = get_current_module_path(__file__, "../test_data/lfs_test_file.txt")
        if not os.path.isfile(self.file_path):
            raise SkipTest

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_is_test_data_file(self):
        self.assertFalse(is_test_data_file(self.file_path))

        self.assertFalse(is_test_data_file(get_current_module_path(__file__)))

        self.assertTrue(is_test_data_file(__file__))

        # self.fail("Test if the TestCase is working.")


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: oxford.map.test_ParametersFile
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.bruker.map.ParametersFile`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.bruker.map.ParametersFile`.
"""

###############################################################################
# Copyright 2012 Hendrix Demers
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

# Local modules.

# Project modules.
from microanalysis_file_format.bruker.map.parameters_file import ParametersFile, DATA_TYPE_UNSIGNED, \
    BYTE_ORDER_DONT_CARE
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.

class TestParametersFile(unittest.TestCase):
    """
    TestCase class for the module `ParametersFile`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.path = get_current_module_path(__file__, "../../../test_data/Bruker/MapRaw")

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_read(self):
        filename = "Sample01.rpl"
        filepath = os.path.join(self.path, filename)
        if not is_test_data_file(filepath):
            raise self.skipTest("File path is not a valid test data file")

        parameters = ParametersFile()
        parameters.read(filepath)

        self.assertEqual(1024, parameters.width)
        self.assertEqual(768, parameters.height)
        self.assertEqual(2048, parameters.depth)
        self.assertEqual(0, parameters.offset)
        self.assertEqual(1, parameters.data_length_B)
        self.assertEqual(DATA_TYPE_UNSIGNED, parameters.data_type)
        self.assertEqual(BYTE_ORDER_DONT_CARE, parameters.byte_order)
        self.assertEqual("vector", parameters.record_by)

        # self.fail("Test if the testcase is working.")

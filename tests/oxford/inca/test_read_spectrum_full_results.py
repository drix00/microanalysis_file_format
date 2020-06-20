#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.oxford.inca.test_ReadSpectrumFullResults
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.ReadSpectrumFullResults`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.ReadSpectrumFullResults`.
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

# Local modules.

# Project modules.
from microanalysis_file_format.oxford.inca.read_spectrum_full_results import ReadSpectrumFullResults, is_valid_file
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.

class TestReadSpectrumFullResults(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../../test_data/SpectrumFullResults 10.txt")
        if not is_test_data_file(self.filepath):
            raise self.skipTest("File path is not a valid test data file")

        self.results = ReadSpectrumFullResults(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        results = ReadSpectrumFullResults(self.filepath)

        assert len(results.data) > 0

    def test_read(self):
        self.results.read(self.filepath)

        data = self.results.data

        self.assertAlmostEquals(0.0088, data["O"][2], 4)

        self.assertAlmostEquals(0.28664, data["Zr"][2], 5)

        self.assertAlmostEquals(100.00, data["Totals"], 2)

        self.assertTrue(True)

    def test_isValidFile(self):
        folder_path = get_current_module_path(__file__, "../../../test_data")

        filepath = os.path.join(folder_path, "SpectrumFullResults 10.txt")
        self.assertEqual(True, is_valid_file(filepath))

        filepath = os.path.join(folder_path, "SpectrumProcessing 10.txt")
        self.assertEqual(False, is_valid_file(filepath))

        filepath = os.path.join(folder_path, "AllSpectra.txt")
        self.assertEqual(False, is_valid_file(filepath))

        self.assertTrue(True)

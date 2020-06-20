#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.oxford.inca.test_ReadSpectrumProcessingResults
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.ReadSpectrumProcessingResults`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.ReadSpectrumProcessingResults`.
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
from microanalysis_file_format.oxford.inca.read_spectrum_processing_results import ReadSpectrumProcessingResults, \
    is_valid_file
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.

class TestReadSpectrumProcessingResults(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../../test_data/SpectrumProcessing 10.txt")
        if not is_test_data_file(self.filepath):
            raise self.skipTest("File path is not a valid test data file")

        self.results = ReadSpectrumProcessingResults(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        results = ReadSpectrumProcessingResults(self.filepath)

        assert len(results.data) > 0

    def test_read(self):
        self.results.read(self.filepath)

        data = self.results.data

        self.assertEqual("", data["Element"][1])

        self.assertEqual("Zr", data["Element"][-1])

        self.assertAlmostEquals(-34864.3, data["Area"][1], 1)

        self.assertAlmostEquals(23655.6, data["Area"][-1], 1)

        self.assertTrue(True)

    def test_isValidFile(self):
        folder_path = get_current_module_path(__file__, "../../../test_data")

        filepath = os.path.join(folder_path, "SpectrumFullResults 10.txt")
        self.assertEqual(False, is_valid_file(filepath))

        filepath = os.path.join(folder_path, "SpectrumProcessing 10.txt")
        self.assertEqual(True, is_valid_file(filepath))

        filepath = os.path.join(folder_path, "AllSpectra.txt")
        self.assertEqual(False, is_valid_file(filepath))

        self.assertTrue(True)

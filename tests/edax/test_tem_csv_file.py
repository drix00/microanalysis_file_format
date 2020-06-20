#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: edax.test_TemCsvFile
   :synopsis: Tests for the module :py:mod:`edax.TemCsvFile`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`edax.TemCsvFile`.
"""

###############################################################################
# Copyright 2009 Hendrix Demers
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

# Third party modules.

# Local modules.

# Project modules.
import microanalysis_file_format.edax.tem_csv_file as TemCsvFile
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.

class TestTemCsvFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathRef = get_current_module_path(__file__, "../../test_data/TEM_Edax/OVERALL.CSV")
        if not is_test_data_file(self.filepathRef):
            raise self.skipTest("File path is not a valid test data file")

        self.data = TemCsvFile.TemCsvFile(self.filepathRef)

        self.numberPoints = 1024

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_Constructor(self):
        self.assertEqual(self.filepathRef, self.data._filepath)

        self.assert_(True)

    def test_read_data(self):
        data = self.data._read_data(self.filepathRef)

        channels = data[TemCsvFile.CHANNEL]
        counts = data[TemCsvFile.COUNTS]
        self.assertEqual(self.numberPoints, len(channels))
        self.assertEqual(self.numberPoints, len(counts))

        self.assertEqual(1024, channels[-1])
        self.assertEqual(775, counts[-1])

        self.assert_(True)

    def test_get_data(self):
        energies_eV, counts = self.data.get_data()

        self.assertEqual(self.numberPoints, len(energies_eV))
        self.assertEqual(self.numberPoints, len(counts))

        self.assertEqual(10240.0, energies_eV[-1])
        self.assertEqual(775, counts[-1])

        self.assert_(True)

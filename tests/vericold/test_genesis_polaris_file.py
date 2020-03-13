#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.vericold.test_genesisPolarisFile
   :synopsis: Tests for the module :py:mod:`pySpectrumFileFormat.vericold.genesisPolarisFile`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`pySpectrumFileFormat.vericold.genesisPolarisFile`.
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

# Third party modules.

# Local modules.

# Project modules.
from pySpectrumFileFormat.vericold.genesis_polaris_file import GenesisPolarisFile
from pySpectrumFileFormat import get_current_module_path, is_test_data_file

# Globals and constants variables.


class TestGenesisPolarisFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../test_data/vericold/k3670_30keV_OFeCalibration.csp")
        if not is_test_data_file(self.filepath):  # pragma: no cover
            raise self.skipTest("Test file not found.")

        self.gp_file = GenesisPolarisFile()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        gp_file = GenesisPolarisFile()

        self.assertEqual(False, gp_file.is_file_read)

        gp_file = GenesisPolarisFile(self.filepath)

        self.assertEqual(True, gp_file.is_file_read)

        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_readFile(self):
        self.assertEqual(False, self.gp_file.is_file_read)

        self.gp_file.read_file(self.filepath)

        self.assertEqual(True, self.gp_file.is_file_read)

    def test_readHeader(self):
        header = self.gp_file.read_header(self.filepath)

        self.assertEqual(1001, header["version"])

        self.assertEqual(3072, header["pixOffset"])

        self.assertEqual(0, header["pixSize"])

        self.assertEqual(3072, header["dataOffset"])

        self.assertEqual(19724, header["dataSize"])

        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_get_spectrum(self):
        gp_file = GenesisPolarisFile(self.filepath)

        energies_eV, intensities = gp_file.get_spectrum()
        self.assertEqual(20000, len(energies_eV))
        self.assertEqual(20000, len(intensities))

        energies_eV, intensities = gp_file.get_spectrum(eV_channel=5.0, limits=(10, 1000))
        self.assertEqual(198, len(energies_eV))
        self.assertEqual(198, len(intensities))

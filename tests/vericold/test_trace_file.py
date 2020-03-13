#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: vericold.test_trace_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`vericold.trace_file`.
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
from pySpectrumFileFormat.vericold.trace_file import TraceFile
from pySpectrumFileFormat import get_current_module_path, is_test_data_file

# Globals and constants variables.


class TestTraceFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../test_data/vericold/test01.trc")
        if not is_test_data_file(self.filepath):  # pragma: no cover
            raise self.skipTest("Test file not found.")

        self.trace_file = TraceFile(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        trace_file = TraceFile(self.filepath)

        self.assertTrue(os.path.isfile(trace_file.filename))

        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetFileSize(self):
        self.assertEqual(3253456, self.trace_file.get_file_size())

        # self.trace_file.print_file_time()

        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_read_trace(self):
        header, times_ms, data = self.trace_file.read_trace(1)
        self.assertEqual(24, len(header))
        self.assertEqual(1000, len(times_ms))
        self.assertEqual(1000, len(data))

    def test_read_header(self):
        self.assertEqual(0, len(self.trace_file.header))
        self.trace_file.read_header()
        self.assertEqual(31, len(self.trace_file.header))

    def test_compute_baseline(self):
        header, times_ms, data = self.trace_file.read_trace(1)
        baseline = self.trace_file.compute_baseline(times_ms, data)
        self.assertAlmostEqual(-896.848, baseline)

    def test_get_pulse(self):
        times_ms, pulse_data = self.trace_file.get_pulse(1)
        self.assertEqual(1000, len(times_ms))
        self.assertEqual(1000, len(pulse_data))

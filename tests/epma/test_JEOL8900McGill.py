#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.epma.test_JEOL8900McGill
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.epma.JEOL8900McGill`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.epma.JEOL8900McGill`.
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
import warnings

# Third party modules.

# Local modules.

# Project modules.
import microanalysis_file_format.epma.JEOL8900McGill as JEOL8900McGill
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.

class TestJEOL8900McGill(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter("ignore")

        unittest.TestCase.setUp(self)

        project_path = get_current_module_path(__file__)

        self.filename = os.path.join(project_path, "../../test_data/data0407.ful")
        if not is_test_data_file(self.filename):
            raise self.skipTest("File is not a test data file")

        self.line_scan_file = JEOL8900McGill.JEOL8900McGill(self.filename)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        self.assertTrue(True)

    def testReadResultsFile(self):
        line_scan_file = JEOL8900McGill.JEOL8900McGill(self.filename)

        number_lines = line_scan_file.read_results_file(self.filename)

        self.assertEqual(5276, number_lines)

        self.assertTrue(True)

    def testReadMasterHeader(self):
        line = "Intensity & Wt. %      Group : Lang            Sample : Song             Page 1 \n"

        self.line_scan_file.read_master_header(line)

        self.assertEqual(self.line_scan_file.masterHeader, {})

        self.assertTrue(True)

    def testReadPointData(self):
        lines = """Unknown Specimen No. 1178
 Group        : Lang            Sample  : Song
 UNK No.      : 1178            Comment : Line 255 AlMgZn-region3
 Stage        :    X=   62.9595  Y=   54.2735  Z=    9.8025
 Acc. Voltage :    15.0 (kV)    Probe Dia. : 0    Scan : Off
 Dated on Apr 11 16:22 2007
 WDS only       No. of accumulation : 1

Curr.(A) : 1.999E-08
Element Peak(mm)    Net(cps)  Bg-(cps)  Bg+(cps)   S.D.(%)   D.L.(ppm)
 1 Al    90.637        -0.3      23.6      17.0    300.00 ?     86
 2 Mg   107.784     30962.1      30.5      33.5      0.38      153
 3 Zn   133.173       242.3      13.7       7.1      4.48      507


Element  f(chi)    If/Ip     abs-el    1/s-el      r-el      c/k-el    c/k-std
 Mg      0.7796    0.0000    0.8997    1.0116     0.9959     1.1033     1.1033
 Zn      0.7657    0.0508    1.1682    0.7385     1.1311     0.9752     0.9752

Element  El. Wt%   Ox Wt%   Norm El%  Norm ox%  At prop    k-value   k-(std)
 Al       0.00      0.00      0.00      0.00     0.000   0.00000  -0.00001 ?
 Mg      96.40     96.40     95.94     95.94    98.451   0.88308   0.88308
 Zn       4.08      4.08      4.06      4.06     1.549   0.04183   0.04183
 -----------------------------------------------------------------------------
Total:  100.48    100.48    100.00    100.00   100.000




""".splitlines()

        self.line_scan_file.read_point_data(lines)

        spectrum_id = 1178
        group = "Lang"
        sample = "Song"
        number = 1178
        comment = "Line 255 AlMgZn-region3"
        stage_x = 62.9595
        stage_y = 54.2735
        stage_z = 9.8025
        incident_energy_keV = 15.0
        probe_diameter = 0
        scan_on = False
        date = "Apr 11 16:22 2007"
        detector_type = "WDS only"
        number_accumulation = 1

        current_A = 1.999E-08

        # Test experimental condition.
        point = self.line_scan_file.points[1178]
        self.assertEqual(spectrum_id, point.spectrum_id)

        self.assertEqual(group, point.group)

        self.assertEqual(sample, point.sample)

        self.assertEqual(number, point.number)

        self.assertEqual(comment, point.comment)

        self.assertEqual(stage_x, point.stage_x)

        self.assertEqual(stage_y, point.stage_y)

        self.assertEqual(stage_z, point.stage_z)

        self.assertEqual(incident_energy_keV, point.incident_energy_keV)

        self.assertEqual(probe_diameter, point.probe_diameter)

        self.assertEqual(scan_on, point.scan_on)

        self.assertEqual(date, point.date)

        self.assertEqual(detector_type, point.detector_type)

        self.assertEqual(number_accumulation, point.number_accumulation)

        self.assertEqual(current_A, point.current_A)

        # Test intensities lines.
        self.assertEqual(300.0, point.element_data['Al']['sd_%%'])

        self.assertEqual(86.0, point.element_data['Al']['dl_ppm'])

        self.assertEqual(30962.1, point.element_data['Mg']['net_cps'])

        self.assertEqual(3, point.element_data['Zn']['id'])

        self.assertEqual(507.0, point.element_data['Zn']['dl_ppm'])

        # Test correction lines.
        self.assertEqual(0.0000, point.element_data['Mg']['If/Ip'])

        self.assertEqual(1.1033, point.element_data['Mg']['c/k-el'])

        self.assertEqual(0.7657, point.element_data['Zn']['f(chi)'])

        self.assertEqual(0.9752, point.element_data['Zn']['c/k-std'])

        # Test concentration lines.
        self.assertEqual(-0.00001, point.element_data['Al']['k-std'])

        self.assertEqual(98.451, point.element_data['Mg']['Atomic'])

        self.assertEqual(4.08, point.element_data['Zn']['El fw'])

        self.assertEqual(0.04183, point.element_data['Zn']['k-value'])

        # Test total line.
        self.assertEqual(100.48, point.element_data['total']['El fw'])

        self.assertEqual(100.0, point.element_data['total']['Atomic'])

        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

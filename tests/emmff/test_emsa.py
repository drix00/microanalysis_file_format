#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.emmff.test_emsa
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.emmff.emsa`

.. moduleauthor:: Philippe T. Pinard <philippe.pinard@gmail.com>

Tests for the module :py:mod:`microanalysis_file_format.emmff.emsa`.
"""

###############################################################################
# Copyright 2011 Philippe T. Pinard
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
import tempfile
import os
from six import PY2, PY3

# Third party modules.

# Local modules.
from microanalysis_file_format import get_current_module_path

# Project modules.
import microanalysis_file_format.emmff.emsa as emsa

# Globals and constants variables.


class TestEmsaReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        filepath = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")
        if not os.path.isfile(filepath):
            raise self.skipTest("File path is not a valid test data file")
        if PY3:
            with open(filepath, 'r', newline="\r\n") as f:
                self.emsa = emsa.read(f)
        elif PY2:
            with open(filepath, 'rb') as f:
                self.emsa = emsa.read(f)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        self.assertEqual(1024, len(self.emsa.y_data))

    def test_is_line_keyword(self):
        reader = emsa.EmsaReader()

        line = ""
        self.assertEqual(False, reader._is_line_keyword(line), msg="Empty line")

        line = None
        self.assertEqual(False, reader._is_line_keyword(line), msg="None line")

        line = "#keyword"
        self.assertEqual(True, reader._is_line_keyword(line), msg="With leading #")

        line = "  #keyword"
        self.assertEqual(True, reader._is_line_keyword(line), msg="With leading space + #")

        line = "\t#keyword"
        self.assertEqual(True, reader._is_line_keyword(line), msg="With leading space + #")

        line = "1#keyword"
        self.assertEqual(False, reader._is_line_keyword(line), msg="With invalid line")

        line = "1.2, 0.2"
        self.assertEqual(False, reader._is_line_keyword(line), msg="With invalid line")

        line = "1.2 0.2"
        self.assertEqual(False, reader._is_line_keyword(line), msg="With invalid line")

    def test_parse_keyword_line(self):
        reader = emsa.EmsaReader()

        line = r"#FORMAT      : EMSA/MAS Spectral Data File"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("FORMAT", keyword)
        self.assertEqual("", comment)
        self.assertEqual("EMSA/MAS Spectral Data File", value)

        line = r"#VERSION     : 1.0"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("VERSION", keyword)
        self.assertEqual("", comment)
        self.assertEqual('1.0', value)

        line = r"#TITLE       : Spectrum 1"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("TITLE", keyword)
        self.assertEqual("", comment)
        self.assertEqual("Spectrum 1", value)

        line = r"#DATE        : 20-NOV-2006"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("DATE", keyword)
        self.assertEqual("", comment)
        self.assertEqual("20-NOV-2006", value)

        line = r"#TIME        : 16:03"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("TIME", keyword)
        self.assertEqual("", comment)
        self.assertEqual("16:03", value)

        line = r"#X_POSITION mm: 0.0000"
        keyword, comment, value = reader._parse_keyword_line(line)
        self.assertEqual("X_POSITION", keyword)
        self.assertEqual("mm", comment)
        self.assertEqual('0.0000', value)

    def test_parse_data_line(self):
        reader = emsa.EmsaReader()

        line = r"-0.200, 0."
        values = reader._parse_data_line(line)
        self.assertEqual(2, len(values))
        self.assertEqual(-0.2, values[0])
        self.assertEqual(0.0, values[1])

        line = r"-0.200 0."
        values = reader._parse_data_line(line)
        self.assertEqual(2, len(values))
        self.assertEqual(-0.2, values[0])
        self.assertEqual(0.0, values[1])

        line = r"-0.200"
        values = reader._parse_data_line(line)
        self.assertEqual(1, len(values))
        self.assertEqual(-0.2, values[0])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0"
        values = reader._parse_data_line(line)
        self.assertEqual(5, len(values))
        self.assertEqual(1.0, values[0])
        self.assertEqual(5.0, values[-1])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0, 6.0"
        values = reader._parse_data_line(line)
        self.assertEqual(6, len(values))
        self.assertEqual(1.0, values[0])
        self.assertEqual(6.0, values[-1])

    def test_format(self):
        self.assertEqual("EMSA/MAS Spectral Data File", self.emsa.header.format)

    def test_version(self):
        self.assertEqual(1.0, self.emsa.header.version)

    def test_title(self):
        self.assertEqual("Spectrum 1", self.emsa.header.title)

    def test_date(self):
        self.assertEqual("20-NOV-2006", self.emsa.header.date)

    def test_time(self):
        self.assertEqual("16:03", self.emsa.header.time)

    def test_owner(self):
        self.assertEqual("helen", self.emsa.header.owner)

    def test_number_points(self):
        self.assertEqual(1024.0, self.emsa.header.number_points)

    def test_number_columns(self):
        self.assertEqual(1.0, self.emsa.header.ncolumns)

    def test_x_units(self):
        self.assertEqual("keV", self.emsa.header.xunits)

    def test_y_units(self):
        self.assertEqual("counts", self.emsa.header.yunits)

    def test_data_type(self):
        self.assertEqual("XY", self.emsa.header.datatype)

    def test_x_per_channel(self):
        self.assertEqual(0.02, self.emsa.header.xperchan)

    def test_offset(self):
        self.assertEqual(-0.2, self.emsa.header.offset)

    def test_signal_type(self):
        self.assertEqual("EDS", self.emsa.header.signaltype)

    def test_channel_offset(self):
        self.assertEqual(10.0, self.emsa.header.choffset)

    def test_live_time(self):
        self.assertEqual(0.34635, self.emsa.header.livetime)

    def test_real_time(self):
        self.assertEqual(0.453241, self.emsa.header.realtime)

    def test_beam_energy(self):
        self.assertEqual(5.0, self.emsa.header.beamkv)

    def test_probe_current(self):
        self.assertEqual(0.0, self.emsa.header.probecur)

    def test_magnification(self):
        self.assertEqual(250.0, self.emsa.header.magcam)

    def test_x_position(self):
        self.assertEqual(0.0, self.emsa.header.xposition[0])
        self.assertEqual('mm', self.emsa.header.xposition[1])

    def test_y_position(self):
        self.assertEqual(0.0, self.emsa.header.yposition[0])
        self.assertEqual('mm', self.emsa.header.yposition[1])

    def test_z_position(self):
        self.assertEqual(0.0, self.emsa.header.zposition[0])
        self.assertEqual('mm', self.emsa.header.zposition[1])


class TestEmsaWriter(unittest.TestCase):
    LINES = ['#FORMAT      : EMSA/MAS Spectral Data File',
             '#VERSION     : 1.0',
             '#TITLE       : Test EMSA file',
             '#DATE        : 14-MAY-2011',
             '#TIME        : 10:10',
             '#OWNER       : John Doe',
             '#NPOINTS     : 5',
             '#NCOLUMNS    : 2',
             '#XUNITS      : eV',
             '#YUNITS      : counts',
             '#DATATYPE    : XY',
             '#XPERCHAN    : 1',
             '#OFFSET      : 0',
             '#SPECTRUM    : Spectral Data Starts Here',
             '0, 10',
             '1, 20',
             '2, 30',
             '3, 40',
             '4, 50',
             '#ENDOFDATA   :',
             '#CHECKSUM    : 21860']

    def setUp(self):
        unittest.TestCase.setUp(self)

        spectrum = self._create_emsa()

        if PY3:
            self.f = tempfile.NamedTemporaryFile('w', delete=False, newline="\r\n")
        elif PY2:
            self.f = tempfile.NamedTemporaryFile('w', delete=False)
        emsa.write(spectrum, self.f)
        self.f.close()

    @staticmethod
    def _create_emsa():
        spectrum = emsa.Emsa()
        spectrum.x_data = [0, 1, 2, 3, 4]
        spectrum.y_data = [10, 20, 30, 40, 50]

        spectrum.header.title = 'Test EMSA file'
        spectrum.header.date = '14-MAY-2011'
        spectrum.header.time = '10:10'
        spectrum.header.owner = 'John Doe'
        spectrum.header.npoints = 5
        spectrum.header.ncolumns = 2
        spectrum.header.xunits = 'eV'
        spectrum.header.yunits = 'counts'
        spectrum.header.datatype = emsa.DATA_TYPE_XY
        spectrum.header.xperchan = 1
        spectrum.header.offset = 0

        spectrum.validate()

        return spectrum

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        os.remove(self.f.name)

    def test_skeleton(self):
        self.assertTrue(True)

    def test_lines(self):
        if PY3:
            with open(self.f.name, 'r', newline="\r\n") as f:
                lines = [line.strip() for line in f.readlines()]
        elif PY2:
            with open(self.f.name, 'rb') as f:
                lines = [line.strip() for line in f.readlines()]

        self.assertEqual(len(lines), len(self.LINES))

        for expected, actual in zip(self.LINES, lines):
            self.assertEqual(expected, actual)

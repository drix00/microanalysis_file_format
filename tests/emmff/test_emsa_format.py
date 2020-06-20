#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.emmff.test_emsaFormat
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.emmff.emsaFormat`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.emmff.emsaFormat`.
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
import sys
import os.path

# Third party modules.

# Local modules.

# Project modules.
import microanalysis_file_format.emmff.emsa_format as emsaFormat
from microanalysis_file_format import get_current_module_path

# Globals and constants variables.


class EmsaFormatTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")
        if not os.path.isfile(self.filepath):
            raise self.skipTest("File path is not a valid test data file")

        self.emsa = emsaFormat.EmsaFormat(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_constructor(self):
        emsaFormat.EmsaFormat()

        self.assertTrue(True)

    def test_read_file(self):
        filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")

        self.emsa.open(filename)

        self.assertNotEqual(0, len(self.emsa.lines))

        self.assertEqual(1054, len(self.emsa.lines))

        filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/BadFile.emsa")

        self.assertRaises(IOError, self.emsa.open, filename)

    def test_is_line_data(self):
        line = ""
        self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="Empty line")
        self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="Empty line")
        self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="Empty line")

        line = None
        self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="None line")
        self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="None line")
        self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="None line")

        self.emsa = emsaFormat.EmsaFormat()
        line = "1.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="Y value")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="Y value")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="Y value")

        line = "1.2, 0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With comma")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With comma")
        self.assertEqual(2, self.emsa.is_line_data(line)[2], msg="With comma")

        line = "1.2 0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With space")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With space")
        self.assertEqual(2, self.emsa.is_line_data(line)[2], msg="With space")

        line = "1.2\t0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With tab")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With tab")
        self.assertEqual(2, self.emsa.is_line_data(line)[2], msg="With tab")

        line = "0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 1 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 1 column")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With 1 column")

        line = "0.1, 0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 2 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 2 column")
        self.assertEqual(2, self.emsa.is_line_data(line)[2], msg="With 2 column")

        line = "0.1, 0.2, 0.3"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 3 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 3 column")
        self.assertEqual(3, self.emsa.is_line_data(line)[2], msg="With 3 column")

        line = "0.1, 0.2, 0.3, 0.4"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 4 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 4 column")
        self.assertEqual(4, self.emsa.is_line_data(line)[2], msg="With 4 column")

        line = "0.1, 0.2, 0.3, 0.4, 0.5"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 5 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 5 column")
        self.assertEqual(5, self.emsa.is_line_data(line)[2], msg="With 5 column")

        line = "0.1, 0.2, 0.3, 0.4, 0.5, 0.6"
        self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="With 6 column")
        self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="With 6 column")
        self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="With 6 column")

        line = "0.1 0.2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 2 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 2 column")
        self.assertEqual(2, self.emsa.is_line_data(line)[2], msg="With 2 column")

        line = "0.1 0.2 0.3"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 3 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 3 column")
        self.assertEqual(3, self.emsa.is_line_data(line)[2], msg="With 3 column")

        line = "0.1 0.2 0.3 0.4"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 4 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 4 column")
        self.assertEqual(4, self.emsa.is_line_data(line)[2], msg="With 4 column")

        line = "0.1 0.2 0.3 0.4 0.5"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With 5 column")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With 5 column")
        self.assertEqual(5, self.emsa.is_line_data(line)[2], msg="With 5 column")

        line = "0.1 0.2 0.3 0.4 0.5 0.6"
        self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="With 6 column")
        self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="With 6 column")
        self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="With 6 column")

        line = "2"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With integer")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With integer")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With integer")

        line = ".1"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="Without leading zero")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="Without leading zero")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="Without leading zero")

        line = "1.0E-6"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With scientific notation")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With scientific notation")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With scientific notation")

        line = "1.0e6"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With scientific notation")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With scientific notation")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With scientific notation")

        line = "1.0d6"
        if sys.platform == 'win32' and "32 bit" in sys.version:
            self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With bad character")
            self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With bad character")
            self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With bad character")
        elif sys.platform == 'win32' and "64 bit" in sys.version:
            self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="With bad character")
            self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="With bad character")
            self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="With bad character")
        else:
            self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="With bad character")
            self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="With bad character")
            self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="With bad character")

        line = "#1.0"
        self.assertEqual(False, self.emsa.is_line_data(line)[0], msg="With leading #")
        self.assertEqual(None, self.emsa.is_line_data(line)[1], msg="With leading #")
        self.assertEqual(0, self.emsa.is_line_data(line)[2], msg="With leading #")

        line = "    0.1"
        self.assertEqual(True, self.emsa.is_line_data(line)[0], msg="With leading space")
        self.assertEqual('Y', self.emsa.is_line_data(line)[1], msg="With leading space")
        self.assertEqual(1, self.emsa.is_line_data(line)[2], msg="With leading space")

        line = "         0.0000,             0.0,"
        flag, mode, number = self.emsa.is_line_data(line)
        self.assertEqual(True, flag, msg="With leading space")
        self.assertEqual('Y', mode, msg="With leading space")
        self.assertEqual(2, number, msg="With leading space")

    def test_is_line_keyword(self):
        line = ""
        self.assertEqual(False, self.emsa.is_line_keyword(line), msg="Empty line")

        line = None
        self.assertEqual(False, self.emsa.is_line_keyword(line), msg="None line")

        line = "#keyword"
        self.assertEqual(True, self.emsa.is_line_keyword(line), msg="With leading #")

        line = "    #keyword"
        self.assertEqual(True, self.emsa.is_line_keyword(line), msg="With leading space + #")

        line = "\t#keyword"
        self.assertEqual(True, self.emsa.is_line_keyword(line), msg="With leading space + #")

        line = "1#keyword"
        self.assertEqual(False, self.emsa.is_line_keyword(line), msg="With invalid line")

        line = "1.2, 0.2"
        self.assertEqual(False, self.emsa.is_line_keyword(line), msg="With invalid line")

        line = "1.2 0.2"
        self.assertEqual(False, self.emsa.is_line_keyword(line), msg="With invalid line")

    def test_read_keyword_line(self):
        line = r"#FORMAT      : EMSA/MAS Spectral Data File"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("FORMAT", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("EMSA/MAS Spectral Data File", data)

        line = r"#VERSION     : 1.0"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("VERSION", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("1.0", data)

        line = r"#TITLE       : Spectrum 1"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("TITLE", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("Spectrum 1", data)

        line = r"#DATE        : 20-NOV-2006"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("DATE", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("20-NOV-2006", data)

        line = r"#TIME        : 16:03"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("TIME", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("16:03", data)

        line = r"#XPOSITION mm: 0.0000"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("XPOSITION", keyword)
        self.assertEqual("mm", keyword_comment)
        self.assertEqual("0.0000", data)

        line = r"##OXINSTELEMS: 6,8,12"
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual("OXINSTELEMS", keyword)
        self.assertEqual("", keyword_comment)
        self.assertEqual("6,8,12", data)

        line = r"-0.200, 0."
        keyword, keyword_comment, data = self.emsa.read_keyword_line(line)
        self.assertEqual(None, keyword)
        self.assertEqual(None, keyword_comment)
        self.assertEqual(None, data)

    def test_read_data_line(self):
        line = r"-0.200, 0."
        values = self.emsa.read_data_line(line)
        self.assertEqual(2, len(values))
        self.assertEqual(-0.2, values[0])
        self.assertEqual(0.0, values[1])

        line = r"-0.200 0."
        values = self.emsa.read_data_line(line)
        self.assertEqual(2, len(values))
        self.assertEqual(-0.2, values[0])
        self.assertEqual(0.0, values[1])

        line = r"-0.200"
        values = self.emsa.read_data_line(line)
        self.assertEqual(1, len(values))
        self.assertEqual(-0.2, values[0])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0"
        values = self.emsa.read_data_line(line)
        self.assertEqual(5, len(values))
        self.assertEqual(1.0, values[0])
        self.assertEqual(5.0, values[-1])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0, 6.0"
        values = self.emsa.read_data_line(line)
        self.assertEqual(6, len(values))
        self.assertEqual(1.0, values[0])
        self.assertEqual(6.0, values[-1])

        line = r"#VERSION         : 1.0"
        values = self.emsa.read_data_line(line)
        self.assertEqual(None, values)

    def test_read_line(self):
        emsa = emsaFormat.EmsaFormat()

        line = r"-0.200, 0."
        emsa.read_line(line)
        self.assertEqual(1, len(emsa.values))
        self.assertEqual(-0.2, emsa.values[0][0])
        self.assertEqual(0.0, emsa.values[0][1])

        line = r"#FORMAT            : EMSA/MAS Spectral Data File"
        emsa.read_line(line)
        self.assertEqual(1, len(emsa.keywords))
        self.assertEqual("FORMAT", emsa.keywords[0]["keyword"])
        self.assertEqual(1, emsa.keywords[0]["order"])

        line = r"#VERSION         : 1.0"
        emsa.read_line(line)
        self.assertEqual(2, len(emsa.keywords))
        self.assertEqual("VERSION", emsa.keywords[1]["keyword"])
        self.assertEqual(2, emsa.keywords[1]["order"])

        line = r"#TITLE             : Spectrum 1"
        emsa.read_line(line)
        self.assertEqual(3, len(emsa.keywords))
        self.assertEqual("TITLE", emsa.keywords[2]["keyword"])
        self.assertEqual(3, emsa.keywords[2]["order"])

    def test_read_lines(self):
        emsa = emsaFormat.EmsaFormat()

        filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")

        emsa.open(filename)

        emsa.read_lines()

        self.assertEqual(30, len(emsa.keywords))

        self.assertEqual(1024, len(emsa.values))

    def test_set_get_format(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_format())

        self.assertEqual("EMSA/MAS Spectral Data File", self.emsa.get_format())

    def test_is_file_valid(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.is_file_valid)

        self.assertEqual(True, self.emsa.is_file_valid)

    def test_set_get_version(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_version())

        self.assertEqual("1.0", self.emsa.get_version())

    def test_set_get_title(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_title())

        self.assertEqual("Spectrum 1", self.emsa.get_title())

    def test_set_get_date(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_date())

        self.assertEqual("20-NOV-2006", self.emsa.get_date())

    def test_set_get_time(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_time())

        self.assertEqual("16:03", self.emsa.get_time())

    def test_set_get_owner(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_owner())

        self.assertEqual("helen", self.emsa.get_owner())

    def test_set_get_number_points(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_number_points())

        self.assertEqual(1024.0, self.emsa.get_number_points())

    def test_set_get_number_columns(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_number_columns())

        self.assertEqual(1.0, self.emsa.get_number_columns())

    def test_set_get_x_units(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_x_units())

        self.assertEqual("keV", self.emsa.get_x_units())

    def test_set_get_y_units(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_y_units())

        self.assertEqual("counts", self.emsa.get_y_units())

    def test_set_get_data_type(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_data_type())

        self.assertEqual("XY", self.emsa.get_data_type())

    def test_set_get_x_per_channel(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_x_per_channel())

        self.assertEqual(0.02, self.emsa.get_x_per_channel())

    def test_set_get_offset(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_offset())

        self.assertEqual(-0.2, self.emsa.get_offset())

    def test_set_get_signal_type(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_signal_type())

        self.assertEqual("EDS", self.emsa.get_signal_type())

    def test_set_get_channel_offset(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_channel_offset())

        self.assertEqual(10.0, self.emsa.get_channel_offset())

    def test_set_get_live_time(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_live_time())

        self.assertEqual(0.34635, self.emsa.get_live_time())

    def test_set_get_real_time(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_real_time())

        self.assertEqual(0.453241, self.emsa.get_real_time())

    def test_set_get_beam_energy(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_beam_energy())

        self.assertEqual(5.0, self.emsa.get_beam_energy())

    def test_set_get_probe_current(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_probe_current())

        self.assertEqual(0.0, self.emsa.get_probe_current())

    def test_set_get_magnification(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_magnification())

        self.assertEqual(250.0, self.emsa.get_magnification())

    def test_set_get_x_position(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_x_position())

        self.assertEqual(0.0, self.emsa.get_x_position())

    def test_set_get_y_position(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_y_position())

        self.assertEqual(0.0, self.emsa.get_y_position())

    def test_set_get_z_position(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_z_position())

        self.assertEqual(0.0, self.emsa.get_z_position())

    def test_set_get_oxford_instruments_element(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_oxford_instruments_element())

        self.assertEqual("6,8,12", self.emsa.get_oxford_instruments_element())

    def test_set_get_oxford_instruments_label(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEqual(None, emsa.get_oxford_instruments_label())

        self.assertEqual("8, 0.525, O", self.emsa.get_oxford_instruments_label())

    def test_create_x_data(self):
        x_data = self.emsa.create_x_data(1024, -0.2, 0.02)
        self.assertEqual(1024, len(x_data))

        x_data_ref = self.emsa.get_data_x()
        self.assertEqual(1024, len(x_data_ref))

        self.assertAlmostEquals(x_data_ref[0], x_data[0])
        self.assertAlmostEquals(x_data_ref[10], x_data[10])
        self.assertAlmostEquals(x_data_ref[-1], x_data[-1])
        self.assertAlmostEquals(x_data_ref[-10], x_data[-10])

    def test_read_file_tem_bruker(self):
        filename = get_current_module_path(__file__, "../../test_data/TEM_Bruker/Gold-pt 2-2.msa")
        if not os.path.isfile(filename):
            raise self.skipTest("File path is not a valid test data file")

        emsa = emsaFormat.EmsaFormat()
        emsa.open(filename)
        emsa.read_lines()
        emsa.set_header()
        emsa.set_spectrum_data()

        self.assertNotEqual(0, len(emsa.lines))

        self.assertEqual(1055, len(emsa.lines))

        self.assertEqual(1024, len(emsa.values))
        self.assertEqual(4096, len(emsa.get_data_x()))
        self.assertEqual(4096, len(emsa.get_data_y()))

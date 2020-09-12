#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.emmff.test_emsa_format
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.emmff.emsa_format`.
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
import os.path
import sys

# Third party modules.
import pytest

# Project modules.
from microanalysis_file_format import get_current_module_path
from microanalysis_file_format.emmff.emsa_format import EmsaFormat
from tests import is_test_data_file

# Local modules.

# Globals and constants variables.


@pytest.fixture
def spectrum1_emsa_file_path():
    file_path = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def spectrum1_emsa_data(spectrum1_emsa_file_path):
    data = EmsaFormat(spectrum1_emsa_file_path)
    return data


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_constructor():
    EmsaFormat()


def test_read_file(spectrum1_emsa_data):
    filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")

    spectrum1_emsa_data.open(filename)

    assert len(spectrum1_emsa_data.lines) != 0

    assert len(spectrum1_emsa_data.lines) == 1054

    filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/BadFile.emsa")

    with pytest.raises(IOError):
        spectrum1_emsa_data.open(filename)


def test_is_line_data(spectrum1_emsa_data):
    line = ""
    assert spectrum1_emsa_data.is_line_data(line)[0] is False, "Empty line"
    assert spectrum1_emsa_data.is_line_data(line)[1] is None, "Empty line"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "Empty line"

    line = None
    assert spectrum1_emsa_data.is_line_data(line)[0] is False, "None line"
    assert spectrum1_emsa_data.is_line_data(line)[1] is None, "None line"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "None line"

    spectrum1_emsa_data = EmsaFormat()
    line = "1.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "Y value"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "Y value"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "Y value"

    line = "1.2, 0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With comma"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With comma"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 2, "With comma"

    line = "1.2 0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With space"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With space"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 2, "With space"

    line = "1.2\t0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With tab"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With tab"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 2, "With tab"

    line = "0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 1 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 1 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With 1 column"

    line = "0.1, 0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 2 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 2 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 2, "With 2 column"

    line = "0.1, 0.2, 0.3"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 3 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 3 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 3, "With 3 column"

    line = "0.1, 0.2, 0.3, 0.4"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 4 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 4 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 4, "With 4 column"

    line = "0.1, 0.2, 0.3, 0.4, 0.5"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 5 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 5 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 5, "With 5 column"

    line = "0.1, 0.2, 0.3, 0.4, 0.5, 0.6"
    assert spectrum1_emsa_data.is_line_data(line)[0] is False, "With 6 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] is None, "With 6 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "With 6 column"

    line = "0.1 0.2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 2 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 2 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 2, "With 2 column"

    line = "0.1 0.2 0.3"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 3 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 3 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 3, "With 3 column"

    line = "0.1 0.2 0.3 0.4"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 4 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 4 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 4, "With 4 column"

    line = "0.1 0.2 0.3 0.4 0.5"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With 5 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With 5 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 5, "With 5 column"

    line = "0.1 0.2 0.3 0.4 0.5 0.6"
    assert spectrum1_emsa_data.is_line_data(line)[0] is False, "With 6 column"
    assert spectrum1_emsa_data.is_line_data(line)[1] is None, "With 6 column"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "With 6 column"

    line = "2"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With integer"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With integer"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With integer"

    line = ".1"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "Without leading zero"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "Without leading zero"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "Without leading zero"

    line = "1.0E-6"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With scientific notation"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With scientific notation"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With scientific notation"

    line = "1.0e6"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With scientific notation"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With scientific notation"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With scientific notation"

    line = "1.0d6"
    if sys.platform == 'win32' and "32 bit" in sys.version:
        assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With bad character"
    elif sys.platform == 'win32' and "64 bit" in sys.version:
        assert spectrum1_emsa_data.is_line_data(line)[0] is False, "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[1] is None, "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "With bad character"
    else:
        assert spectrum1_emsa_data.is_line_data(line)[0] is False, "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[1] is None, "With bad character"
        assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "With bad character"

    line = "#1.0"
    assert spectrum1_emsa_data.is_line_data(line)[0] is False, "With leading #"
    assert spectrum1_emsa_data.is_line_data(line)[1] is None, "With leading #"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 0, "With leading #"

    line = "    0.1"
    assert spectrum1_emsa_data.is_line_data(line)[0] is True, "With leading space"
    assert spectrum1_emsa_data.is_line_data(line)[1] == 'Y', "With leading space"
    assert spectrum1_emsa_data.is_line_data(line)[2] == 1, "With leading space"

    line = "         0.0000,             0.0,"
    flag, mode, number = spectrum1_emsa_data.is_line_data(line)
    assert flag is True, "With leading space"
    assert mode == 'Y', "With leading space"
    assert number == 2, "With leading space"


def test_is_line_keyword(spectrum1_emsa_data):
    line = ""
    assert spectrum1_emsa_data.is_line_keyword(line) is False, "Empty line"

    line = None
    assert spectrum1_emsa_data.is_line_keyword(line) is False, "None line"

    line = "#keyword"
    assert spectrum1_emsa_data.is_line_keyword(line) is True, "With leading #"

    line = "    #keyword"
    assert spectrum1_emsa_data.is_line_keyword(line) is True, "With leading space + #"

    line = "\t#keyword"
    assert spectrum1_emsa_data.is_line_keyword(line) is True, "With leading space + #"

    line = "1#keyword"
    assert spectrum1_emsa_data.is_line_keyword(line) is False, "With invalid line"

    line = "1.2, 0.2"
    assert spectrum1_emsa_data.is_line_keyword(line) is False, "With invalid line"

    line = "1.2 0.2"
    assert spectrum1_emsa_data.is_line_keyword(line) is False, "With invalid line"


def test_read_keyword_line(spectrum1_emsa_data):
    line = r"#FORMAT      : EMSA/MAS Spectral Data File"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword == "FORMAT"
    assert keyword_comment == ""
    assert data == "EMSA/MAS Spectral Data File"

    line = r"#VERSION     : 1.0"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword == "VERSION"
    assert keyword_comment == ""
    assert data == "1.0"

    line = r"#TITLE       : Spectrum 1"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword == "TITLE"
    assert keyword_comment == ""
    assert data == "Spectrum 1"

    line = r"#DATE        : 20-NOV-2006"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword == "DATE"
    assert keyword_comment == ""
    assert data == "20-NOV-2006"

    line = r"#TIME        : 16:03"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword == "TIME"
    assert keyword_comment == ""
    assert data == "16:03"

    line = r"#XPOSITION mm: 0.0000"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    # noinspection SpellCheckingInspection
    assert keyword == "XPOSITION"
    assert keyword_comment == "mm"
    assert data == "0.0000"

    line = r"##OXINSTELEMS: 6,8,12"
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    # noinspection SpellCheckingInspection
    assert keyword == "OXINSTELEMS"
    assert keyword_comment == ""
    assert data == "6,8,12"

    line = r"-0.200, 0."
    keyword, keyword_comment, data = spectrum1_emsa_data.read_keyword_line(line)
    assert keyword is None
    assert keyword_comment is None
    assert data is None


def test_read_data_line(spectrum1_emsa_data):
    line = r"-0.200, 0."
    values = spectrum1_emsa_data.read_data_line(line)
    assert len(values) == 2
    assert values[0] == -0.2
    assert values[1] == 0.0

    line = r"-0.200 0."
    values = spectrum1_emsa_data.read_data_line(line)
    assert len(values) == 2
    assert values[0] == -0.2
    assert values[1] == 0.0

    line = r"-0.200"
    values = spectrum1_emsa_data.read_data_line(line)
    assert len(values) == 1
    assert values[0] == -0.2

    line = r"1.0, 2.0, 3.0, 4.0, 5.0"
    values = spectrum1_emsa_data.read_data_line(line)
    assert len(values) == 5
    assert values[0] == 1.0
    assert values[-1] == 5.0

    line = r"1.0, 2.0, 3.0, 4.0, 5.0, 6.0"
    values = spectrum1_emsa_data.read_data_line(line)
    assert len(values) == 6
    assert values[0] == 1.0
    assert values[-1] == 6.0

    line = r"#VERSION         : 1.0"
    values = spectrum1_emsa_data.read_data_line(line)
    assert values is None


def test_read_line():
    emsa = EmsaFormat()

    line = r"-0.200, 0."
    emsa.read_line(line)
    assert len(emsa.values) == 1
    assert emsa.values[0][0] == -0.2
    assert emsa.values[0][1] == 0.0

    line = r"#FORMAT            : EMSA/MAS Spectral Data File"
    emsa.read_line(line)
    assert len(emsa.keywords) == 1
    assert emsa.keywords[0]["keyword"] == "FORMAT"
    assert emsa.keywords[0]["order"] == 1

    line = r"#VERSION         : 1.0"
    emsa.read_line(line)
    assert len(emsa.keywords) == 2
    assert emsa.keywords[1]["keyword"] == "VERSION"
    assert emsa.keywords[1]["order"] == 2

    line = r"#TITLE             : Spectrum 1"
    emsa.read_line(line)
    assert len(emsa.keywords) == 3
    assert emsa.keywords[2]["keyword"] == "TITLE"
    assert emsa.keywords[2]["order"] == 3


def test_read_lines():
    emsa = EmsaFormat()

    filename = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")

    emsa.open(filename)

    emsa.read_lines()

    assert len(emsa.keywords) == 30

    assert len(emsa.values) == 1024


def test_set_get_format(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_format() is None

    assert spectrum1_emsa_data.get_format() == "EMSA/MAS Spectral Data File"


def test_is_file_valid(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.is_file_valid is None

    assert spectrum1_emsa_data.is_file_valid is True


def test_set_get_version(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_version() is None

    assert spectrum1_emsa_data.get_version() == "1.0"


def test_set_get_title(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_title() is None

    assert spectrum1_emsa_data.get_title() == "Spectrum 1"


def test_set_get_date(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_date() is None

    assert spectrum1_emsa_data.get_date() == "20-NOV-2006"


def test_set_get_time(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_time() is None

    assert spectrum1_emsa_data.get_time() == "16:03"


def test_set_get_owner(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_owner() is None

    assert spectrum1_emsa_data.get_owner() == "helen"


def test_set_get_number_points(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_number_points() is None

    assert spectrum1_emsa_data.get_number_points() == 1024.0


def test_set_get_number_columns(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_number_columns() is None

    assert spectrum1_emsa_data.get_number_columns() == 1.0


def test_set_get_x_units(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_x_units() is None

    assert spectrum1_emsa_data.get_x_units() == "keV"


def test_set_get_y_units(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_y_units() is None

    assert spectrum1_emsa_data.get_y_units() == "counts"


def test_set_get_data_type(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_data_type() is None

    assert spectrum1_emsa_data.get_data_type() == "XY"


def test_set_get_x_per_channel(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_x_per_channel() is None

    assert spectrum1_emsa_data.get_x_per_channel() == 0.02


def test_set_get_offset(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_offset() is None

    assert spectrum1_emsa_data.get_offset() == -0.2


def test_set_get_signal_type(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_signal_type() is None

    assert spectrum1_emsa_data.get_signal_type() == "EDS"


def test_set_get_channel_offset(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_channel_offset() is None

    assert spectrum1_emsa_data.get_channel_offset() == 10.0


def test_set_get_live_time(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_live_time() is None

    assert spectrum1_emsa_data.get_live_time() == 0.34635


def test_set_get_real_time(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_real_time() is None

    assert spectrum1_emsa_data.get_real_time() == 0.453241


def test_set_get_beam_energy(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_beam_energy() is None

    assert spectrum1_emsa_data.get_beam_energy() == 5.0


def test_set_get_probe_current(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_probe_current() is None

    assert spectrum1_emsa_data.get_probe_current() == 0.0


def test_set_get_magnification(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_magnification() is None

    assert spectrum1_emsa_data.get_magnification() == 250.0


def test_set_get_x_position(spectrum1_emsa_data):
    emsa = EmsaFormat()

    assert emsa.get_x_position() is None

    assert spectrum1_emsa_data.get_x_position() == 0.0


def test_set_get_y_position(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_y_position() is None

    assert spectrum1_emsa_data.get_y_position() == 0.0


def test_set_get_z_position(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_z_position() is None

    assert spectrum1_emsa_data.get_z_position() == 0.0


def test_set_get_oxford_instruments_element(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_oxford_instruments_element() is None

    assert spectrum1_emsa_data.get_oxford_instruments_element() == "6,8,12"


def test_set_get_oxford_instruments_label(spectrum1_emsa_data):
    emsa = EmsaFormat()
    assert emsa.get_oxford_instruments_label() is None

    assert spectrum1_emsa_data.get_oxford_instruments_label() == "8, 0.525, O"


def test_create_x_data(spectrum1_emsa_data):
    x_data = spectrum1_emsa_data.create_x_data(1024, -0.2, 0.02)
    assert len(x_data) == 1024

    x_data_ref = spectrum1_emsa_data.get_data_x()
    assert len(x_data_ref) == 1024

    assert x_data[0] == pytest.approx(x_data_ref[0])
    assert x_data[10] == pytest.approx(x_data_ref[10])
    assert x_data[-1] == pytest.approx(x_data_ref[-1])
    assert x_data[-10] == pytest.approx(x_data_ref[-10])


def test_read_file_tem_bruker():
    filename = get_current_module_path(__file__, "../../test_data/TEM_Bruker/Gold-pt 2-2.msa")
    if not os.path.isfile(filename):
        raise pytest.skip("File path is not a valid test data file")

    emsa = EmsaFormat()
    emsa.open(filename)
    emsa.read_lines()
    emsa.set_header()
    emsa.set_spectrum_data()

    assert len(emsa.lines) != 0

    assert len(emsa.lines) == 1055

    assert len(emsa.values) == 1024
    assert len(emsa.get_data_x()) == 4096
    assert len(emsa.get_data_y()) == 4096

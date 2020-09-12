#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.emmff.test_emsa
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
from six import PY2, PY3

# Third party modules.
import pytest

# Local modules.
from microanalysis_file_format import get_current_module_path

# Project modules.
import microanalysis_file_format.emmff.emsa as emsa
from tests import is_test_data_file

# Globals and constants variables.


@pytest.fixture
def spectrum1_emsa_file_path():
    file_path = get_current_module_path(__file__, "../../test_data/emmff/spectra/spectrum1.emsa")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def spectrum1_emsa_data(spectrum1_emsa_file_path):
    if PY3:
        with open(spectrum1_emsa_file_path, 'r', newline="\r\n") as f:
            data = emsa.read(f)
    elif PY2:
        with open(spectrum1_emsa_file_path, 'rb') as f:
            data = emsa.read(f)
    return data


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_number_data(spectrum1_emsa_data):
    assert len(spectrum1_emsa_data.y_data) == 1024


def test_is_line_keyword():
    reader = emsa.EmsaReader()

    line = ""
    assert reader._is_line_keyword(line) is False, "Empty line"

    line = None
    assert reader._is_line_keyword(line) is False, "None line"

    line = "#keyword"
    assert reader._is_line_keyword(line) is True, "With leading #"

    line = "  #keyword"
    assert reader._is_line_keyword(line) is True, "With leading space + #"

    line = "\t#keyword"
    assert reader._is_line_keyword(line) is True, "With leading space + #"

    line = "1#keyword"
    assert reader._is_line_keyword(line) is False, "With invalid line"

    line = "1.2, 0.2"
    assert reader._is_line_keyword(line) is False, "With invalid line"

    line = "1.2 0.2"
    assert reader._is_line_keyword(line) is False, "With invalid line"


def test_parse_keyword_line():
    reader = emsa.EmsaReader()

    line = r"#FORMAT      : EMSA/MAS Spectral Data File"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "FORMAT"
    assert comment == ""
    assert value == "EMSA/MAS Spectral Data File"

    line = r"#VERSION     : 1.0"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "VERSION"
    assert comment == ""
    assert value == '1.0'

    line = r"#TITLE       : Spectrum 1"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "TITLE"
    assert comment == ""
    assert value == "Spectrum 1"

    line = r"#DATE        : 20-NOV-2006"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "DATE"
    assert comment == ""
    assert value == "20-NOV-2006"

    line = r"#TIME        : 16:03"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "TIME"
    assert comment == ""
    assert value == "16:03"

    line = r"#X_POSITION mm: 0.0000"
    keyword, comment, value = reader._parse_keyword_line(line)
    assert keyword == "X_POSITION"
    assert comment == "mm"
    assert value == '0.0000'


def test_parse_data_line():
    reader = emsa.EmsaReader()

    line = r"-0.200, 0."
    values = reader._parse_data_line(line)
    assert len(values) == 2
    assert values[0] == -0.2
    assert values[1] == 0.0

    line = r"-0.200 0."
    values = reader._parse_data_line(line)
    assert len(values) == 2
    assert values[0] == -0.2
    assert values[1] == 0.0

    line = r"-0.200"
    values = reader._parse_data_line(line)
    assert len(values) == 1
    assert values[0] == -0.2

    line = r"1.0, 2.0, 3.0, 4.0, 5.0"
    values = reader._parse_data_line(line)
    assert len(values) == 5
    assert values[0] == 1.0
    assert values[-1] == 5.0

    line = r"1.0, 2.0, 3.0, 4.0, 5.0, 6.0"
    values = reader._parse_data_line(line)
    assert len(values) == 6
    assert values[0] == 1.0
    assert values[-1] == 6.0


def test_format(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.format == "EMSA/MAS Spectral Data File"


def test_version(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.version == 1.0


def test_title(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.title == "Spectrum 1"


def test_date(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.date == "20-NOV-2006"


def test_time(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.time == "16:03"


def test_owner(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.owner == "helen"


def test_number_points(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.number_points == 1024.0


def test_number_columns(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.ncolumns == 1.0


def test_x_units(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.xunits == "keV"


def test_y_units(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.yunits == "counts"


def test_data_type(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.datatype == "XY"


def test_x_per_channel(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.xperchan == 0.02


def test_offset(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.offset == -0.2


def test_signal_type(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.signaltype == "EDS"


def test_channel_offset(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.choffset == 10.0


def test_live_time(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.livetime == 0.34635


def test_real_time(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.realtime == 0.453241


def test_beam_energy(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.beamkv == 5.0


def test_probe_current(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.probecur == 0.0


def test_magnification(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.magcam == 250.0


def test_x_position(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.xposition[0] == 0.0
    assert spectrum1_emsa_data.header.xposition[1] == 'mm'


def test_y_position(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.yposition[0] == 0.0
    assert spectrum1_emsa_data.header.yposition[1] == 'mm'


def test_z_position(spectrum1_emsa_data):
    assert spectrum1_emsa_data.header.zposition[0] == 0.0
    assert spectrum1_emsa_data.header.zposition[1] == 'mm'


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


@pytest.fixture
def created_emsa_file_path(tmpdir):
    spectrum = _create_emsa()
    file_path = tmpdir / "spectrum1.emsa"

    if PY3:
        with open(file_path, 'w', newline="\r\n") as f:
            emsa.write(spectrum, f)
    elif PY2:
        with open(file_path, 'wb') as f:
            emsa.write(spectrum, f)
    return file_path


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


def test_lines(created_emsa_file_path):
    if PY3:
        with open(created_emsa_file_path, 'r', newline="\r\n") as f:
            lines = [line.strip() for line in f.readlines()]
    elif PY2:
        with open(created_emsa_file_path, 'rb') as f:
            lines = [line.strip() for line in f.readlines()]

    assert len(lines), len(LINES)

    for expected, actual in zip(LINES, lines):
        assert actual == expected

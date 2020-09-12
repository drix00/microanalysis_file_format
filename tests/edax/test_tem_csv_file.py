#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.edax.test_tem_csv_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.edax.tem_csv_file`.
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from microanalysis_file_format.edax.tem_csv_file import TemCsvFile, CHANNEL, COUNTS
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def overall_csv_file_path():
    file_path = get_current_module_path(__file__, "../../test_data/TEM_Edax/OVERALL.CSV")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def overall_csv_data(overall_csv_file_path):
    data = TemCsvFile(overall_csv_file_path)
    return data


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


# self.numberPoints = 1024

def test_constructor(overall_csv_file_path, overall_csv_data):
    assert overall_csv_data._filepath == overall_csv_file_path


def test_read_data(overall_csv_file_path, overall_csv_data):
    data = overall_csv_data._read_data(overall_csv_file_path)

    channels = data[CHANNEL]
    counts = data[COUNTS]
    assert len(channels) == 1024
    assert len(counts) == 1024

    assert channels[-1] == 1024
    assert counts[-1] == 775


def test_get_data(overall_csv_data):
    energies_eV, counts = overall_csv_data.get_data()

    assert len(energies_eV) == 1024
    assert len(counts) == 1024

    assert energies_eV[-1] == 10240.0
    assert counts[-1] == 775

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.oxford.inca.test_read_all_spectrum_results
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.read_all_spectrum_results`.
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from microanalysis_file_format.oxford.inca.read_all_spectrum_results import ReadAllSpectrumResults, is_valid_file
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file

# Globals and constants variables.


@pytest.fixture
def all_spectra_file_path():
    file_path = get_current_module_path(__file__, "../../../test_data/AllSpectra.txt")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def all_spectra_data(all_spectra_file_path):
    data = ReadAllSpectrumResults(all_spectra_file_path)
    return data


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_constructor(all_spectra_file_path):
    results = ReadAllSpectrumResults(all_spectra_file_path)

    assert len(results.data) > 0


def test_read(all_spectra_file_path, all_spectra_data):
    all_spectra_data.read(all_spectra_file_path)

    data = all_spectra_data.data

    assert data["Spectrum 5"][1] == pytest.approx(0.853, 3)

    assert data["Spectrum 5"][-1] == pytest.approx(100.000, 3)

    assert data["Minimum"][1] == pytest.approx(0.520, 3)

    assert data["Minimum"][-1] == pytest.approx(15.128, 3)


def test_extract_min_data(all_spectra_data):
    # line = "Min.    19.086    0.520    4.404    0.598    40.670    14.894    15.128     "
    line = "Min.\t19.086\t0.520\t4.404\t0.598\t40.670\t14.894\t15.128\t"
    results = all_spectra_data._extract_line_data(line)

    assert results[1] == pytest.approx(0.520, 3)

    assert results[-1] == pytest.approx(15.128, 3)


def test_is_valid_file():
    folder_path = get_current_module_path(__file__, "../../../test_data")

    filepath = os.path.join(folder_path, "SpectrumFullResults 10.txt")
    assert is_valid_file(filepath) is False

    filepath = os.path.join(folder_path, "SpectrumProcessing 10.txt")
    assert is_valid_file(filepath) is False

    filepath = os.path.join(folder_path, "AllSpectra.txt")
    assert is_valid_file(filepath) is True

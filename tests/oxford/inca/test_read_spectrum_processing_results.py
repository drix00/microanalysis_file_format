#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.oxford.inca.test_read_spectrum_processing_results
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.oxford.inca.read_spectrum_processing_results`.
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
from microanalysis_file_format.oxford.inca.read_spectrum_processing_results import ReadSpectrumProcessingResults, \
    is_valid_file
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def spectrum_processing_file_path():
    file_path = get_current_module_path(__file__, "../../../test_data/SpectrumProcessing 10.txt")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def spectrum_processing_data(spectrum_processing_file_path):
    data = ReadSpectrumProcessingResults(spectrum_processing_file_path)
    return data


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_constructor(spectrum_processing_file_path):
    results = ReadSpectrumProcessingResults(spectrum_processing_file_path)

    assert len(results.data) > 0


def test_read(spectrum_processing_file_path, spectrum_processing_data):
    spectrum_processing_data.read(spectrum_processing_file_path)

    data = spectrum_processing_data.data

    assert data["Element"][1] == ""
    assert data["Element"][-1] == "Zr"
    assert data["Area"][1] == pytest.approx(-34864.3, 1)
    assert data["Area"][-1] == pytest.approx(23655.6, 1)


def test_is_valid_file():
    folder_path = get_current_module_path(__file__, "../../../test_data")

    filepath = os.path.join(folder_path, "SpectrumFullResults 10.txt")
    assert is_valid_file(filepath) is False

    filepath = os.path.join(folder_path, "SpectrumProcessing 10.txt")
    assert is_valid_file(filepath) is True

    filepath = os.path.join(folder_path, "AllSpectra.txt")
    assert is_valid_file(filepath) is False

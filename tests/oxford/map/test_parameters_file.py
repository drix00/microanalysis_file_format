#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.oxford.map.test_parameters_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for module `microanalysis_file_format.oxford.map.parameters_file`.
"""

###############################################################################
# Copyright 2012 Hendrix Demers
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
from microanalysis_file_format.oxford.map.parameters_file import ParametersFile, DATA_TYPE_UNSIGNED, \
    BYTE_ORDER_DONT_CARE, DATA_TYPE_SIGNED, BYTE_ORDER_LITTLE_ENDIAN
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file

# Globals and constants variables.


@pytest.fixture
def raw_map_path():
    path = get_current_module_path(__file__, "../../../test_data/OxfordInstruments/MapRaw")
    if not os.path.isdir(path):  # pragma: no cover
        pytest.skip("Invalid test data folder")

    return path


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(raw_map_path):
    filename = "Map30kV.rpl"
    filepath = os.path.join(raw_map_path, filename)
    if not is_test_data_file(filepath):
        pytest.skip("File path is not a valid test data file")

    parameters = ParametersFile()
    parameters.read(filepath)

    assert parameters.width == 512
    assert parameters.height == 384
    assert parameters.depth == 2048
    assert parameters.offset == 0
    assert parameters.data_length_B == 1
    assert parameters.data_type == DATA_TYPE_UNSIGNED
    assert parameters.byte_order == BYTE_ORDER_DONT_CARE
    assert parameters.record_by == "IMAGE \"Site of Interest 1\""

    filename = "Project 1.rpl"
    filepath = os.path.join(raw_map_path, filename)

    parameters = ParametersFile()
    parameters.read(filepath)

    assert parameters.width == 512
    assert parameters.height == 384
    assert parameters.depth == 2048
    assert parameters.offset == 0
    assert parameters.data_length_B == 2
    assert parameters.data_type == DATA_TYPE_SIGNED
    assert parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN
    assert parameters.record_by == "IMAGE \"Site of Interest 1\""

    filename = "mapSOI_15.rpl"
    filepath = os.path.join(raw_map_path, filename)

    parameters = ParametersFile()
    parameters.read(filepath)

    assert parameters.width == 512
    assert parameters.height == 384
    assert parameters.depth == 2048
    assert parameters.offset == 0
    assert parameters.data_length_B == 4
    assert parameters.data_type == DATA_TYPE_SIGNED
    assert parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN
    assert parameters.record_by == "IMAGE \"Site of Interest 15\""

    filename = "mapSOI14.rpl"
    filepath = os.path.join(raw_map_path, filename)

    parameters = ParametersFile()
    parameters.read(filepath)

    assert parameters.width == 512
    assert parameters.height == 384
    assert parameters.depth == 2048
    assert parameters.offset == 0
    assert parameters.data_length_B == 4
    assert parameters.data_type == DATA_TYPE_SIGNED
    assert parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN
    assert parameters.record_by == "IMAGE \"Site of Interest 14\""

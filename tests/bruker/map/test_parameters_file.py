#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule::microanalysis_file_format.bruker.map.test_parameters_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.bruker.map.parameters_file`.
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from microanalysis_file_format.bruker.map.parameters_file import ParametersFile, DATA_TYPE_UNSIGNED, \
    BYTE_ORDER_DONT_CARE
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def sample01_file_path():
    file_path = get_current_module_path(__file__, "../../../test_data/Bruker/MapRaw/Sample01.rpl")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read(sample01_file_path):
    parameters = ParametersFile()
    parameters.read(sample01_file_path)

    assert parameters.width == 1024
    assert parameters.height == 768
    assert parameters.depth == 2048
    assert parameters.offset == 0
    assert parameters.data_length_B == 1
    assert parameters.data_type == DATA_TYPE_UNSIGNED
    assert parameters.byte_order == BYTE_ORDER_DONT_CARE
    assert parameters.record_by == "vector"

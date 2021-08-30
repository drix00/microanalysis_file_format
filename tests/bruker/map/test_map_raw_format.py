#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.bruker.map.test_map_raw_format
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.bruker.map.map_raw_format`.
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
import numpy as np

# Local modules.

# Project modules.

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_indexes():
    data = np.arange(12).reshape(3, 4)

    assert data.shape == (3, 4)
    assert data[0, 0] == 0.0
    assert data[2, 3] == 11

    values = data[:, 1]
    assert np.all(values == np.array([1, 5, 9]))

    indices = (Ellipsis, 1)
    values = data[indices]
    assert np.all(values == np.array([1, 5, 9]))

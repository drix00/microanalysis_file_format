#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.vericold.test_genesisPolarisFile
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.vericold.genesisPolarisFile`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.vericold.genesisPolarisFile`.
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

# Third party modules.
import pytest

# Local modules.

# Project modules.
from microanalysis_file_format.vericold.genesis_polaris_file import GenesisPolarisFile
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def spectrum_csp():
    file_path = get_current_module_path(__file__, "../../test_data/vericold/k3670_30keV_OFeCalibration.csp")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def line_scan_pls():
    file_path = get_current_module_path(__file__, "../../test_data/vericold/line_scan_01.pls")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def map_psd():
    # noinspection SpellCheckingInspection
    file_path = get_current_module_path(__file__, "../../test_data/vericold/oxyde_scale.psd")
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


def test_constructor(spectrum_csp):
    gp_file = GenesisPolarisFile()
    assert gp_file.is_file_read is False

    gp_file = GenesisPolarisFile(spectrum_csp)
    assert gp_file.is_file_read is True


def test_read_file(spectrum_csp):
    gp_file = GenesisPolarisFile()
    assert gp_file.is_file_read is False

    gp_file.read_file(spectrum_csp)
    assert gp_file.is_file_read is True


def test_read_file_bad_file():
    gp_file = GenesisPolarisFile()

    assert gp_file.is_file_read is False

    file_path = "bad_file_does_not_exist.csp"
    gp_file.read_file(file_path)

    assert gp_file.is_file_read is False


def test_read_header(spectrum_csp):
    gp_file = GenesisPolarisFile()
    header = gp_file.read_header(spectrum_csp)

    assert header["version"] == 1001
    assert header["pixOffset"] == 3072
    assert header["pixSize"] == 0
    assert header["dataOffset"] == 3072
    assert header["dataSize"] == 19724


def test_get_spectrum(spectrum_csp):
    gp_file = GenesisPolarisFile(spectrum_csp)

    # noinspection PyPep8Naming
    energies_eV, intensities = gp_file.get_spectrum()
    assert len(energies_eV) == 20000
    assert len(intensities) == 20000

    # noinspection PyPep8Naming
    energies_eV, intensities = gp_file.get_spectrum(eV_channel=5.0, limits=(10, 1000))
    assert len(energies_eV) == 198
    assert len(intensities) == 198


def test_read_file_line_scan_pls(line_scan_pls):
    gp_file = GenesisPolarisFile()

    assert gp_file.is_file_read is False

    gp_file.read_file(line_scan_pls)

    assert gp_file.is_file_read is True


def test_read_file_map_psd(map_psd):
    gp_file = GenesisPolarisFile()

    assert gp_file.is_file_read is False

    gp_file.read_file(map_psd)

    assert gp_file.is_file_read is True

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.epma.test_JEOL8900McGill
   :synopsis: Tests for the module :py:mod:`microanalysis_file_format.epma.JEOL8900McGill`

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.epma.JEOL8900McGill`.
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
from microanalysis_file_format.epma.JEOL8900McGill import JEOL8900McGill
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def data_0407_file_path():
    file_path = get_current_module_path(__file__, "../../test_data/data0407.ful")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def line_scan_file(data_0407_file_path):
    line_scan_file = JEOL8900McGill(data_0407_file_path)
    return line_scan_file


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_read_results_file(data_0407_file_path):
    line_scan_file = JEOL8900McGill(data_0407_file_path)

    number_lines = line_scan_file.read_results_file(data_0407_file_path)

    assert number_lines == 5276


def test_read_master_header(line_scan_file):
    line = "Intensity & Wt. %      Group : Lang            Sample : Song             Page 1 \n"

    line_scan_file.read_master_header(line)

    assert line_scan_file.master_header == {}


def test_read_point_data(line_scan_file):
    lines = """Unknown Specimen No. 1178
 Group        : Lang            Sample  : Song
 UNK No.      : 1178            Comment : Line 255 AlMgZn-region3
 Stage        :    X=   62.9595  Y=   54.2735  Z=    9.8025
 Acc. Voltage :    15.0 (kV)    Probe Dia. : 0    Scan : Off
 Dated on Apr 11 16:22 2007
 WDS only       No. of accumulation : 1

Curr.(A) : 1.999E-08
Element Peak(mm)    Net(cps)  Bg-(cps)  Bg+(cps)   S.D.(%)   D.L.(ppm)
 1 Al    90.637        -0.3      23.6      17.0    300.00 ?     86
 2 Mg   107.784     30962.1      30.5      33.5      0.38      153
 3 Zn   133.173       242.3      13.7       7.1      4.48      507


Element  f(chi)    If/Ip     abs-el    1/s-el      r-el      c/k-el    c/k-std
 Mg      0.7796    0.0000    0.8997    1.0116     0.9959     1.1033     1.1033
 Zn      0.7657    0.0508    1.1682    0.7385     1.1311     0.9752     0.9752

Element  El. Wt%   Ox Wt%   Norm El%  Norm ox%  At prop    k-value   k-(std)
 Al       0.00      0.00      0.00      0.00     0.000   0.00000  -0.00001 ?
 Mg      96.40     96.40     95.94     95.94    98.451   0.88308   0.88308
 Zn       4.08      4.08      4.06      4.06     1.549   0.04183   0.04183
 -----------------------------------------------------------------------------
Total:  100.48    100.48    100.00    100.00   100.000




""".splitlines()

    line_scan_file.read_point_data(lines)

    spectrum_id = 1178
    group = "Lang"
    sample = "Song"
    number = 1178
    comment = "Line 255 AlMgZn-region3"
    stage_x = 62.9595
    stage_y = 54.2735
    stage_z = 9.8025
    # noinspection PyPep8Naming
    incident_energy_keV = 15.0
    probe_diameter = 0
    scan_on = False
    date = "Apr 11 16:22 2007"
    detector_type = "WDS only"
    number_accumulation = 1

    # noinspection PyPep8Naming
    current_A = 1.999E-08

    # Test experimental condition.
    point = line_scan_file.points[1178]
    assert point.spectrum_id == spectrum_id

    assert point.group == group

    assert point.sample == sample

    assert point.number == number

    assert point.comment == comment

    assert point.stage_x == stage_x

    assert point.stage_y == stage_y

    assert point.stage_z == stage_z

    assert point.incident_energy_keV == incident_energy_keV

    assert point.probe_diameter == probe_diameter

    assert point.scan_on == scan_on

    assert point.date == date

    assert point.detector_type == detector_type

    assert point.number_accumulation == number_accumulation

    assert point.current_A == current_A

    # Test intensities lines.
    assert point.element_data['Al']['sd_%%'] == 300.0

    assert point.element_data['Al']['dl_ppm'] == 86.0

    assert point.element_data['Mg']['net_cps'] == 30962.1

    assert point.element_data['Zn']['id'] == 3

    assert point.element_data['Zn']['dl_ppm'] == 507.0

    # Test correction lines.
    assert point.element_data['Mg']['If/Ip'] == 0.0000

    assert point.element_data['Mg']['c/k-el'] == 1.1033

    assert point.element_data['Zn']['f(chi)'] == 0.7657

    assert point.element_data['Zn']['c/k-std'] == 0.9752

    # Test concentration lines.
    assert point.element_data['Al']['k-std'] == -0.00001

    assert point.element_data['Mg']['Atomic'] == 98.451

    assert point.element_data['Zn']['El fw'] == 4.08

    assert point.element_data['Zn']['k-value'] == 0.04183

    # Test total line.
    assert point.element_data['total']['El fw'] == 100.48

    assert point.element_data['total']['Atomic'] == 100.0

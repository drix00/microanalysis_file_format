#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.vericold.test_trace_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`microanalysis_file_format.vericold.trace_file`.
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
from microanalysis_file_format.vericold.trace_file import TraceFile, compute_baseline
from microanalysis_file_format import get_current_module_path
from tests import is_test_data_file


# Globals and constants variables.


@pytest.fixture
def trace_file_path():
    file_path = get_current_module_path(__file__, "../../test_data/vericold/test01.trc")
    if not is_test_data_file(file_path):  # pragma: no cover
        pytest.skip("Invalid test data file")

    return file_path


@pytest.fixture
def trace_file(trace_file_path):
    trace_file = TraceFile(trace_file_path)
    return trace_file


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_constructor(trace_file_path):
    trace_file = TraceFile(trace_file_path)

    assert os.path.isfile(trace_file.filename)


def test_get_file_size(trace_file):
    assert trace_file.get_file_size() == 3253456


def test_read_trace(trace_file):
    header, times_ms, data = trace_file.read_trace(1)
    assert len(header) == 24
    assert len(times_ms) == 1000
    assert len(data) == 1000


def test_read_header(trace_file):
    assert len(trace_file.header) == 0
    trace_file.read_header()
    assert len(trace_file.header) == 31


def test_compute_baseline(trace_file):
    header, times_ms, data = trace_file.read_trace(1)
    baseline = compute_baseline(times_ms, data)
    assert baseline == -896.848


def test_get_pulse(trace_file):
    times_ms, pulse_data = trace_file.get_pulse(1)

    assert len(times_ms) == 1000
    assert len(pulse_data) == 1000


# noinspection SpellCheckingInspection
def test_print_file_time(capsys, trace_file):
    trace_file.print_file_time()
    captured = capsys.readouterr()
    assert len(captured.out.split("\n")) == 4


# noinspection SpellCheckingInspection
def test_print_header(capsys, trace_file_path):
    trace_file = TraceFile(trace_file_path)

    trace_file.read_header()
    trace_file.print_header()
    captured = capsys.readouterr()
    assert captured.out == "Size:  1180\n" \
                           "Version:  1\n" \
                           "CurrentSystemTime_64 113959555061\n" \
                           "CurrentSystemTime_milli 61\n" \
                           "CurrentSystemTime_timezone 300\n" \
                           "CurrentSystemTime_dstflag 0\n" \
                           "Localtime_sec 10\n" \
                           "Localtime_min 19\n" \
                           "Localtime_hour 13\n" \
                           "Localtime_mday 10\n" \
                           "Localtime_mon 1\n" \
                           "Localtime_year 106\n" \
                           "Localtime_wday 5\n" \
                           "Localtime_yday 40\n" \
                           "Localtime_isdst 0\n" \
                           "ClockTime_ms 0\n" \
                           "LiveTime_ms 0\n" \
                           "DeadTime_ms 0\n" \
                           "TraceLength 1024\n" \
                           "SampleRate 0.0\n" \
                           "RegTemperature 0.0\n" \
                           "IBias 0.0\n" \
                           "AmpFactor 0.0\n" \
                           "AccVoltage 0.0\n" \
                           "Aperture 0.0\n" \
                           "WDistance 0.0\n" \
                           "PixelSize 1.5851067981919654e-231\n"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.oxford.inca.ReadAllSpectrumResults
   :synopsis: Read Oxford Instrument all spectrum result file from inca.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read Oxford Instrument all spectrum result file from inca.
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

# Local modules.

# Project modules.

# Globals and constants variables.


class ReadAllSpectrumResults(object):
    _KEYWORD_SEPARATOR = ":"

    _NORMALISED_COMMENT = "All elements analyzed (Normalised)"

    _RESULTS_WEIGHT_PERCENT = "All results in Weight Percent"

    _MEAN = "Mean"
    _STD_DEV = "Std. dev."
    _MAX = "Max."
    _MIN = "Min."

    _SPECTRUM = "Spectrum Label"

    def __init__(self, filepath):
        self.comments = []
        self.data = {}

        self.read(filepath)

        if len(self.data) == 0:
            raise ValueError

    def read(self, filepath):
        lines = open(filepath, 'r').readlines()

        self._extract_data(lines)

    def _extract_data(self, lines):
        read_spectra_state = False

        data = {}
        for line in lines:
            line = line.strip()

            if len(line) == 0:
                continue

            if self._KEYWORD_SEPARATOR in line:
                self._extract_keyword_value(line)
                read_spectra_state = False
            elif self._NORMALISED_COMMENT in line:
                self._add_comment(line)
                read_spectra_state = False
            elif self._RESULTS_WEIGHT_PERCENT in line:
                self._add_comment(line)
                read_spectra_state = False
            elif self._MEAN in line:
                data["Mean"] = self._extract_line_data(line)
                read_spectra_state = False
            elif self._STD_DEV in line:
                data["StdDev"] = self._extract_line_data(line)
                read_spectra_state = False
            elif self._MAX in line:
                data["Maximum"] = self._extract_line_data(line)
                read_spectra_state = False
            elif self._MIN in line:
                data["Minimum"] = self._extract_line_data(line)
                read_spectra_state = False
            elif self._SPECTRUM in line:
                headers = self._extract_spectrum_header(line)
                self.headers = headers
                read_spectra_state = True
            elif read_spectra_state:
                label, new_data = self._extract_spectrum_data(line)
                data[label] = new_data
            else:
                pass

        self.data = data

    @staticmethod
    def _extract_spectrum_data(line):
        items = line.split("\t")

        label = items[0]

        values = []

        # Skip label.
        for item in items[1:]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        return label, values

    @staticmethod
    def _extract_spectrum_header(line):
        items = line.split("\t")

        values = []

        # Skip label.
        for item in items[1:]:
            try:
                value = str(item)

                values.append(value)
            except ValueError:
                pass

        return values

    @staticmethod
    def _extract_line_data(line):
        items = line.split("\t")

        values = []

        # Skip label.
        for item in items[1:]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        return values

    def _extract_keyword_value(self, line):
        # TODO: Implement
        pass

    def _add_comment(self, line):
        self.comments.append(line)


def is_valid_file(filepath):
    try:
        ReadAllSpectrumResults(filepath)

        is_valid = True
    except ValueError:
        is_valid = False

    return is_valid

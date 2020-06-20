#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.oxford.inca.ReadSpectrumFullResults
   :synopsis: Read Oxford Instrument spectrum full result file from inca.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read Oxford Instrument spectrum full result file from inca.
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


class ReadSpectrumFullResults(object):
    _KEYWORD_SEPARATOR = ":"

    _SAMPLE_POLISHED_COMMENT = "Sample is polished"

    _SAMPLE_UNCOATED_COMMENT = "Sample is uncoated"

    _ELEMENT_OPTIMIZATION_COMMENT = "The element used for optimization"

    _ELEMENT = "k ratio"

    _TOTALS = "Totals"

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
        read_elements_state = False

        data = {}
        for line in lines:
            line = line.strip()

            if len(line) == 0:
                continue

            if self._KEYWORD_SEPARATOR in line and not read_elements_state:
                self._extract_keyword_value(line)
                read_elements_state = False
            elif self._SAMPLE_POLISHED_COMMENT in line:
                self._add_comment(line)
                read_elements_state = False
            elif self._SAMPLE_UNCOATED_COMMENT in line:
                self._add_comment(line)
                read_elements_state = False
            elif self._ELEMENT_OPTIMIZATION_COMMENT in line:
                self._add_comment(line)
                read_elements_state = False
            elif self._ELEMENT in line:
                headers = self._extract_header(line)
                self.headers = headers
                read_elements_state = True
            elif self._TOTALS in line:
                data["Totals"] = self._extract_totals_data(line)
                read_elements_state = False
            elif read_elements_state:
                label, new_data = self._extract_spectrum_data(line)
                data[label] = new_data
            else:
                pass

        self.data = data

    @staticmethod
    def _extract_spectrum_data(line):
        items = line.split("\t")

        label = items[0]

        values = [items[1]]

        # Skip label.
        for item in items[2:8]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        for item in items[8:]:
            values.append(item)

        return label, values

    @staticmethod
    def _extract_header(line):
        items = line.split("\t")

        values = []

        for item in items:
            try:
                value = str(item)

                values.append(value)
            except ValueError:
                pass

        return values

    @staticmethod
    def _extract_totals_data(line):
        items = line.split("\t")

        totals = float(items[-1])

        return totals

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
        ReadSpectrumFullResults(filepath)

        is_valid = True
    except ValueError:
        is_valid = False

    return is_valid

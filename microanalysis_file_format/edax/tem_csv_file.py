#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: edax.TemCsvFile
   :synopsis: Read EDAX csv spectrum file from a TEM.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read EDAX csv spectrum file from a TEM.
"""

###############################################################################
# Copyright 2009 Hendrix Demers
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
import csv

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
CHANNEL = "Channel"
COUNTS = "Counts"


class TemCsvFile(object):
    def __init__(self, filepath):
        self._filepath = filepath

        self._data = self._read_data(self._filepath)

    @staticmethod
    def _read_data(filepath):
        reader = csv.reader(open(filepath, 'rU'))

        data = {}
        data.setdefault(CHANNEL, [])
        data.setdefault(COUNTS, [])

        for row in reader:
            channel = int(row[0])
            counts = int(row[1])

            data[CHANNEL].append(channel)
            data[COUNTS].append(counts)

        return data

    def get_channels(self):
        return self._data[CHANNEL]

    def get_energies_eV(self, eV_channel_eV=10.0):
        return [xx * eV_channel_eV for xx in self._data[CHANNEL]]

    def get_counts(self):
        return self._data[COUNTS]

    def get_data(self, eV_channel_eV=10.0):
        return self.get_energies_eV(eV_channel_eV), self.get_counts()

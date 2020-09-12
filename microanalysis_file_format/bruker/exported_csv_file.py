#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.bruker.exported_csv_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read exported bruker csv file.
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
import logging
import csv

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.

KEY_ENERGY = "Primary energy: "
KEY_LIFETIME = "Life time: "
KEY_SPECTRUM = "Spectrum: "
KEY_CHANNEL = "Channel"


class Spectrum(object):
    def __init__(self):
        self.spectrum_name = ""
        self.primary_energy_keV = 0.0
        self.life_time_s = 0.0

        self.channels = []
        self.energies_keV = []
        self.counts_list = []

    @property
    def spectrum_name(self):
        return self._spectrum_name

    @spectrum_name.setter
    def spectrum_name(self, spectrum_name):
        self._spectrum_name = spectrum_name

    @property
    def primary_energy_keV(self):
        return self._primary_energy_keV

    @primary_energy_keV.setter
    def primary_energy_keV(self, primary_energy_keV):
        self._primary_energy_keV = primary_energy_keV

    @property
    def life_time_s(self):
        return self._life_time_s

    @life_time_s.setter
    def life_time_s(self, life_time_s):
        self._life_time_s = life_time_s

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        self._channels = channels

    @property
    def energies_keV(self):
        return self._energies_keV

    @energies_keV.setter
    def energies_keV(self, energies_keV):
        self._energies_keV = energies_keV

    @property
    def counts_list(self):
        return self._counts_list

    @counts_list.setter
    def counts_list(self, counts_list):
        self._counts_list = counts_list


def read_spectrum(filepath):
    logging.info("Reading spectrum: %s", filepath)

    reader = csv.reader(open(filepath, 'rb'))

    spectrum = Spectrum()

    for row in reader:
        if row[0] == KEY_SPECTRUM:
            spectrum.spectrum_name = row[1].strip()

        if row[0] == KEY_ENERGY:
            spectrum.primaryEnergy_keV = float(row[2])

        if row[0] == KEY_LIFETIME:
            if row[3] == "ms":
                spectrum.lifeTime_s = float(row[2])*1.0e-3

        if row[0] == KEY_CHANNEL:
            break

    for row in reader:
        channel = int(row[0])
        energy_keV = float(row[1])
        counts = float(row[2])

        spectrum.channels.append(channel)
        spectrum.energies_keV.append(energy_keV)
        spectrum.counts_list.append(counts)

    assert len(spectrum.channels) == len(spectrum.energies_keV)
    assert len(spectrum.channels) == len(spectrum.counts_list)

    logging.info(spectrum.spectrum_name)
    logging.info(spectrum.primary_energy_keV)
    logging.info(spectrum.lifeTime_s)
    logging.info(len(spectrum.channels))

    return spectrum

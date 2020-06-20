#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: raw_map_bruker

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Example how to read raw map file from Bruker.
"""

# Copyright 2020 Hendrix Demers
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

# Standard library modules.
import os.path

# Third party modules.
import matplotlib.pyplot as plt

# Local modules.

# Project modules.
from microanalysis_file_format.bruker.map.map_raw_format import MapRawFormat

# Globals and constants variables.


def run():
    path = r"F:\backup_su8230\bruker_data\Quantax User\edx\Data\2015\Demopoulos\Christine\D3-900"
    # filename = "Map30kV.raw"
    filename = "D3-900-map4.raw"
    filepath = os.path.join(path, filename)

    map_raw = MapRawFormat(filepath)

    channels, data_cube = map_raw.get_data_cube()
    plt.figure()
    plt.plot(channels, data_cube[100, 100, :])

    line = 150
    column = 150
    x_data, y_data = map_raw.get_spectrum(line, column)

    plt.figure()
    plt.plot(x_data, y_data)

    x_data, y_data = map_raw.get_sum_spectrum()

    plt.figure()
    plt.plot(x_data, y_data)

    path = r"G:\backup_su8000\eds_ebsd\2010-2013-EDS\HDemers\AuCuStandard"
    filename = r"20130701_AuMap.raw"
    filepath = os.path.join(path, filename)

    map_raw = MapRawFormat(filepath)

    channels, data_cube = map_raw.get_data_cube()
    plt.figure()
    plt.plot(channels, data_cube[0, 0, :])

    plt.show()


def run20120307():
    path = r"G:\backup_su8000\eds_ebsd\2010-2013-EDS\HDemers\20120307\rareearthSample"
    filename = "D3-900-map4.raw"
    filepath = os.path.join(path, filename)

    map_raw = MapRawFormat(filepath)

    line = 150
    column = 150
    x_data, y_data = map_raw.get_spectrum(line, column)

    plt.figure()
    plt.plot(x_data, y_data)
    plt.show()


def main():
    run()
    run20120307()


if __name__ == '__main__':  # pragma: no cover
    main()

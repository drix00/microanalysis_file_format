#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: raw_map_oxford

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Example how to read raw map file from Oxford.
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
from microanalysis_file_format.oxford.map.map_raw_format import MapRawFormat

# Globals and constants variables.


def run():
    path = r"I:\archives\results\experiments\SU8000\others\exampleEDS"
    # filename = "Map30kV.raw"
    filename = "Project 1.raw"
    filepath = os.path.join(path, filename)

    map_raw = MapRawFormat(filepath)

    line = 150
    column = 150
    pixel_id = line + column*512
    x_data, y_data = map_raw.get_spectrum(pixel_id=pixel_id)

    plt.figure()
    plt.plot(x_data, y_data)

    x_data, y_data = map_raw.get_sum_spectrum()

    plt.figure()
    plt.plot(x_data, y_data)
    plt.show()


def run20120307():
    path = r"I:\archives\results\experiments\SU8000\hdemers\RareEarths\20120307\rareearthSample"
    filename = "mapSOI_15.raw"
    filepath = os.path.join(path, filename)

    map_raw = MapRawFormat(filepath)

    line = 150
    column = 150
    pixel_id = line + column*512
    x_data, y_data = map_raw.get_spectrum(pixel_id=pixel_id)

    plt.figure()
    plt.plot(x_data, y_data)
    plt.show()


def main():
    run()
    run20120307()


if __name__ == '__main__':  # pragma: no cover
    main()

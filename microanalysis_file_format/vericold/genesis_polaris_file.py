#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.vericold.genesis_polaris_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read genesis polaris file.
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
import struct

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from microanalysis_file_format.vericold import get_file_size

# Globals and constants variables.

# TODO: Test with a Polaris spectrum line scan file .pls
# TODO: Test with a Polaris spectrum mapping file .psd
# TODO: Test if the file size formula match the real file size.


class GenesisPolarisFile(object):
    def __init__(self, filepath=None):

        self.header_size = 3072

        self.header_format = get_header_format()

        # print "header_format size: %i (%i)" % (struct.calcsize(self.header_format), self.header_size)
        assert self.header_size == struct.calcsize(self.header_format)

        self.pixel_times_size = 4

        self.pixel_times_format = "<L"

        # print "pixel_times_size size: %i (%i)" % (struct.calcsize(self.pixel_times_format), self.pixel_times_size)
        assert self.pixel_times_size == struct.calcsize(self.pixel_times_format)

        self.csp_data_size = 8

        self.csp_data_format = "<fL"

        # print "traceDataFormat size: %i (%i)" % (struct.calcsize("<"+self.traceDataFormat), self.traceDataSize)
        assert self.csp_data_size == struct.calcsize(self.csp_data_format)

        self.is_file_read = False
        self.header = {}
        self.pixel_times = {}
        self.file_size = 0
        self.csp_data = None

        self.reset()

        if filepath is not None:
            self.read_file(filepath)

    def reset(self):
        self.is_file_read = False

        self.header = {}

        self.pixel_times = {}


    # TODO: Add the option to read only a fraction of the data for huge file.
    def read_file(self, filepath):
        if os.path.isfile(filepath):
            self.file_size = get_file_size(filepath)

            self.header = self.read_header(filepath)

            number_points = self.header["number_points"]

            number_lines = self.header["number_lines"]

            offset = self.header["pixOffset"]

            self.pixel_times = self.read_pixel_times(filepath, number_points, number_lines, offset)

            csp_data_size = self.header["dataSize"]

            offset = self.header["dataOffset"]

            self.csp_data = self.read_csp_data(filepath, csp_data_size, offset)

            self.is_file_read = True

            return

    def read_csp_data(self, filepath, csp_data_size, offset):
        csp_data = []

        csp_file = open(filepath, "rb")

        csp_file.seek(offset)

        for dummy_index in range(csp_data_size):
            csp_data_str = csp_file.read(self.csp_data_size)

            values = struct.unpack(self.csp_data_format, csp_data_str)

            energy_eV = float(values[0])

            time = values[1]

            csp_data.append((energy_eV, time))

        return csp_data

    def read_pixel_times(self, filepath, number_points, number_lines, offset):
        pixel_times = []

        number_pixels = number_points * number_lines

        csp_file = open(filepath, "rb")

        csp_file.seek(offset)

        for dummy_index in range(number_pixels):
            pixel_times_str = csp_file.read(self.pixel_times_size)

            values = struct.unpack(self.pixel_times_format, pixel_times_str)

            pixel_time = values[0]

            pixel_times.append(pixel_time)

        return pixel_times

    def read_header(self, filepath):
        csp_file = open(filepath, "rb")

        header_str = csp_file.read(self.header_size)

        values = struct.unpack(self.header_format, header_str)

        header = {}

        header["tag"] = values[0]

        header["version"] = values[1]
        header["number_points"] = values[2]
        header["number_lines"] = values[3]

        header["pixOffset"] = values[4]
        header["pixSize"] = values[5]
        header["dataOffset"] = values[6]
        header["dataSize"] = values[7]

        header["dwell"] = float(values[8])

        header["date"] = values[9]

        header["analyzerType"] = values[10]
        header["analysisMode"] = values[11]

        header["preset"] = float(values[12])
        header["live_time"] = float(values[13])
        header["tilt"] = float(values[14])
        header["takeoff"] = float(values[15])
        header["XRayInc"] = float(values[16])
        header["azimuth"] = float(values[17])
        header["elevation"] = float(values[18])
        header["beamCurrent"] = float(values[19])
        header["kV"] = float(values[20])
        header["startEv"] = float(values[21])
        header["endEv"] = float(values[22])
        header["fullscale"] = float(values[23])

        return header

    # TODO: Get spectrum from a pixel.
    def get_spectrum(self, eV_channel=1.0, limits=None):

        if limits is not None:
            start_energy_eV = limits[0]

            end_energy_eV = limits[1]
        else:
            start_energy_eV = self.header["startEv"]

            end_energy_eV = self.header["endEv"]

        energies_eV = np.arange(start_energy_eV, end_energy_eV + eV_channel, eV_channel)

        data = [energy_eV for energy_eV, dummy_time in self.csp_data]

        intensities, bin_edges = np.histogram(data, energies_eV)

        energies_eV = energies_eV[:-1]
        assert len(energies_eV) == len(intensities)

        # print len(self.csp_data), sum(intensities)

        return energies_eV, intensities


def get_header_format():
    header_format = "<"

    # tag[16]
    header_format += "16s"
    # version
    header_format += "3l"

    # pixOffset
    header_format += "4L"

    # dwell
    header_format += "f"

    # TODO: find the correct header_format for date.
    # date
    header_format += "8s"

    # analyzerType
    header_format += "2l"

    # preset
    header_format += "12f"

    # nPeaks
    header_format += "l"

    # TODO: Find the correct header_format for Peaks.
    # Peaks[48]
    header_format += "384s"

    # nRemark
    header_format += "l"

    # TODO: Find the correct header_format for Remarks.
    # Remarks[10]
    header_format += "400s"

    # x
    header_format += "4f"

    # nDetRes
    header_format += "l"

    # detRes[12]
    header_format += "12f"

    # nStartX
    header_format += "4l"

    # Filler[1708]
    header_format += "1708s"

    # matLabel[40]
    header_format += "40s"

    # Filler[2]
    # header_format += "2s"

    # Label[216]
    header_format += "216s"

    # imgFilename[120]
    header_format += "120s"

    # TODO: finish all data in header.

    return header_format

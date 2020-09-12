#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.bruker.map.map_raw_format
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read Bruker Instruments map in the raw format.
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

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from microanalysis_file_format.bruker.map.parameters_file import ParametersFile, BYTE_ORDER_LITTLE_ENDIAN, \
    DATA_TYPE_SIGNED, DATA_TYPE_UNSIGNED, RECORDED_BY_IMAGE, RECORDED_BY_VECTOR

# Globals and constants variables.


class MapRawFormat(object):
    def __init__(self, raw_file_path):
        logging.info("Raw file: %s", raw_file_path)

        self._rawFilepath = raw_file_path
        parameters_file_path = self._rawFilepath.replace('.raw', '.rpl')

        self._parameters = ParametersFile()
        self._parameters.read(parameters_file_path)

        self._data = None

        self._format = self._generate_format(self._parameters)

    @staticmethod
    def _generate_format(parameters):
        spectrum_format = ""
        if parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN:
            spectrum_format += '<'

        if parameters.data_length_B == 1:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "b"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "B"
        elif parameters.data_length_B == 2:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "h"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "H"
        elif parameters.data_length_B == 4:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "i"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "I"

        logging.info("Format: %s", spectrum_format)

        return spectrum_format

    @staticmethod
    def _generate_sum_spectra_format(parameters):
        spectrum_format = ""
        if parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN:
            spectrum_format += '<'

        spectrum_format += '%i' % (parameters.width*parameters.height)

        if parameters.data_length_B == 1:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "b"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "B"
        elif parameters.data_length_B == 2:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "h"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "H"
        elif parameters.data_length_B == 4:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "i"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "I"

        logging.info("Format: %s", spectrum_format)

        return spectrum_format

    @staticmethod
    def _generate_spectra_format_vector(parameters):
        spectrum_format = ""
        if parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN:
            spectrum_format += '<'

        spectrum_format += '{:d}'.format(parameters.depth)

        if parameters.data_length_B == 1:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "b"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "B"
        elif parameters.data_length_B == 2:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "h"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "H"
        elif parameters.data_length_B == 4:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "i"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "I"

        logging.debug("Format: %s", spectrum_format)

        return spectrum_format

    @staticmethod
    def _generate_sum_spectra_format_vector(parameters):
        spectrum_format = ""
        if parameters.byte_order == BYTE_ORDER_LITTLE_ENDIAN:
            spectrum_format += '<'

        number_pixels = parameters.width*parameters.height

        spectrum_format += '%i' % (parameters.depth*number_pixels)

        if parameters.data_length_B == 1:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "b"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "B"
        elif parameters.data_length_B == 2:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "h"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "H"
        elif parameters.data_length_B == 4:
            if parameters.data_type == DATA_TYPE_SIGNED:
                spectrum_format += "i"
            elif parameters.data_type == DATA_TYPE_UNSIGNED:
                spectrum_format += "I"

        logging.debug("Format: %s", spectrum_format)

        return spectrum_format

    def get_spectrum(self, pixel_x, pixel_y):
        image_offset = self._parameters.width*self._parameters.height
        logging.debug("File offset: %i", image_offset)

        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            spectrum = self._data[:, pixel_y, pixel_x]

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            spectrum = self._data[pixel_y, pixel_x, :]

        channels = np.arange(0, self._parameters.depth)

        assert len(channels) == len(spectrum)
        return channels, spectrum

    def get_data_cube(self):

        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            data_cube = self._data[:, :, :]
            print(data_cube.shape)
            data_cube = np.rollaxis(data_cube, 0, 3)
            print(data_cube.shape)

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            data_cube = self._data[:, :, :]

        channels = np.arange(0, self._parameters.depth)

        return channels, data_cube

    def get_roi_spectrum(self, pixel_x_min, pixel_x_max, pixel_y_min, pixel_y_max):
        image_offset = self._parameters.width*self._parameters.height
        logging.debug("File offset: %i", image_offset)

        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            spectrum = np.sum(self._data[:, pixel_y_min:pixel_y_max + 1, pixel_x_min:pixel_x_max + 1], axis=(1, 2))

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            spectrum = np.sum(self._data[pixel_y_min:pixel_y_max + 1, pixel_x_min:pixel_x_max + 1, :], axis=(0, 1))

        channels = np.arange(0, self._parameters.depth)

        assert len(channels) == len(spectrum)
        return channels, spectrum

    def get_sum_spectrum(self):
        x = np.arange(0, self._parameters.depth)
        y = np.zeros_like(x)

        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            raise NotImplementedError

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            y = self._data.sum(axis=(0, 1))

        assert len(x) == len(y)
        return x, y

    def get_total_intensity_image(self):
        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            image = np.sum(self._data, axis=0)

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            image = np.sum(self._data, axis=2)

        return image

    def get_roi_intensity_image(self, channel_range):
        channel_min, channel_max = channel_range

        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            image = np.sum(self._data[channel_min:channel_max, ...], axis=0)

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            image = np.sum(self._data[..., channel_min:channel_max], axis=2)

        return image

    def get_maximum_pixel_spectrum(self):
        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            spectrum = np.amax(self._data, axis=(1, 2))

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            spectrum = np.amax(self._data, axis=(0, 1))

        channels = np.arange(0, self._parameters.depth)

        assert len(channels) == len(spectrum)
        return channels, spectrum

    def get_maximum_pixel_spectrum_pixels(self):
        self._read_data()
        flat_pixels = np.zeros(self._parameters.depth)

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            flat_pixels = np.argmax(self._data, axis=0)

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            for channel in np.arange(0, self._parameters.depth):
                flat_pixels[channel] = np.argmax(self._data[:, :, channel])

        pixels = []
        for pixel in flat_pixels:
            j = int(pixel/self._parameters.width)
            i = int(pixel % self._parameters.width)
            pixels.append((i, j))

        return pixels

    def get_maximum_pixel_spectrum2(self):
        self._read_data()
        channels = np.arange(0, self._parameters.depth)
        spectrum = np.zeros_like(channels)

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            spectrum = np.amax(self._data, axis=(1, 2))

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            for channel in channels:
                spectrum[channel] = np.amax(self._data[:, :, channel])

        assert len(channels) == len(spectrum)
        return channels, spectrum

    def get_total_spectrum(self):
        self._read_data()

        if self._parameters.record_by == RECORDED_BY_IMAGE:
            spectrum = np.sum(self._data, axis=(1, 2))

        elif self._parameters.record_by == RECORDED_BY_VECTOR:
            spectrum = np.sum(self._data, axis=(0, 1))

        channels = np.arange(0, self._parameters.depth)

        assert len(channels) == len(spectrum)
        return channels, spectrum

    def get_parameters(self):
        return self._parameters

    def _read_data(self):
        mmap_mode = 'c'
        if self._data is None:
            if self._parameters.data_type == 'signed':
                data_type = 'int'
            elif self._parameters.data_type == 'unsigned':
                data_type = 'uint'
            elif self._parameters.data_type == 'float':
                pass
            else:
                raise TypeError('Unknown "data-type" string.')

            if self._parameters.byte_order == 'big-endian':
                endian = '>'
            elif self._parameters.byte_order == 'little-endian':
                endian = '<'
            else:
                endian = '='

            data_type = data_type + str(int(self._parameters.data_length_B) * 8)
            data_type = np.dtype(data_type)
            data_type = data_type.newbyteorder(endian)

            self._data = np.memmap(self._rawFilepath, offset=self._parameters.offset, dtype=data_type, mode=mmap_mode)

            if self._parameters.record_by == 'vector':
                shape = (self._parameters.height, self._parameters.width, self._parameters.depth)
                self._data = self._data.reshape(shape)
            elif self._parameters.record_by == 'image':
                shape = (self._parameters.depth, self._parameters.height, self._parameters.width)
                self._data = self._data.reshape(shape)
            elif self._parameters.record_by == 'dont-care':
                shape = (self._parameters.height, self._parameters.width)
                self._data = self._data.reshape(shape)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: oxford.map.MapRawFormat
   :synopsis: Read Oxford Instruments map in the raw format.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read Oxford Instruments map in the raw format.
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
import struct
import logging

# Third party modules.
import numpy as np

# Local modules.

# Project modules.
from microanalysis_file_format.oxford.map.parameters_file import ParametersFile, BYTE_ORDER_LITTLE_ENDIAN, \
    DATA_TYPE_SIGNED, DATA_TYPE_UNSIGNED

# Globals and constants variables.


class MapRawFormat(object):
    def __init__(self, raw_file_path):
        logging.info("Raw file: %s", raw_file_path)

        self._rawFilepath = raw_file_path
        parameters_file_path = self._rawFilepath.replace('.raw', '.rpl')

        self._parameters = ParametersFile()
        self._parameters.read(parameters_file_path)

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

    def get_spectrum(self, pixel_id):
        logging.debug("Pixel ID: %i", pixel_id)

        image_offset = self._parameters.width*self._parameters.height
        logging.debug("File offset: %i", image_offset)

        logging.debug("Size: %i", struct.calcsize(self._format))

        x = np.arange(0, self._parameters.depth)
        y = np.zeros_like(x)
        raw_file = open(self._rawFilepath, 'rb')
        for channel in range(self._parameters.depth):
            file_offset = self._parameters.offset + (pixel_id + channel * image_offset) * self._parameters.data_length_B
            raw_file.seek(file_offset)
            file_buffer = raw_file.read(struct.calcsize(self._format))
            items = struct.unpack(self._format, file_buffer)
            y[channel] = float(items[0])

        raw_file.close()

        return x, y

    def get_sum_spectrum(self):
        x = np.arange(0, self._parameters.depth)
        y = np.zeros_like(x)
        raw_file = open(self._rawFilepath, 'rb')
        file_offset = self._parameters.offset
        raw_file.seek(file_offset)

        sum_spectrum_format = self._generate_sum_spectra_format(self._parameters)

        for channel in range(self._parameters.depth):
            logging.info("Channel: %i", channel)
            file_buffer = raw_file.read(struct.calcsize(sum_spectrum_format))
            items = struct.unpack(sum_spectrum_format, file_buffer)
            y[channel] = np.sum(items)

        raw_file.close()

        return x, y

    def get_sum_spectrum_old(self):
        number_pixels = self._parameters.width*self._parameters.height
        logging.info("Number of pixels: %i", number_pixels)

        x = np.arange(0, self._parameters.depth)
        y_sum = np.zeros_like(x)

        for pixelId in range(number_pixels):
            _x, y = self.get_spectrum(pixelId)
            y_sum += y

        return x, y_sum

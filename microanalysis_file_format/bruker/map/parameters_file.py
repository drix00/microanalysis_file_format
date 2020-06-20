#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: oxford.map.ParametersFile
   :synopsis: Parameters of the raw map file.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Parameters of the raw map file.
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

# Local modules.

# Project modules.

# Globals and constants variables.
DATA_TYPE_UNSIGNED = "unsigned"
DATA_TYPE_SIGNED = "signed"

BYTE_ORDER_DONT_CARE = "dont-care"
BYTE_ORDER_LITTLE_ENDIAN = "little-endian"

RECORDED_BY_IMAGE = "image"
RECORDED_BY_VECTOR = "vector"

KEY_WIDTH = "width"
KEY_HEIGHT = "height"
KEY_DEPTH = "depth"
KEY_OFFSET = "offset"
KEY_DATA_LENGTH_B = "data-length"
KEY_DATA_TYPE = "data-type"
KEY_BYTE_ORDER = "byte-order"
KEY_RECORD_BY = "record-by"
KEY_ENERGY_keV = "E0_kV"
KEY_PIXEL_SIZE_nm = "px_size_nm"


class ParametersFile(object):
    def __init__(self):
        self._parameters = {}

        self.width = None
        self.height = None
        self.depth = None
        self.offset = None
        self.data_length_B = None
        self.data_type = None
        self.byte_order = None
        self.record_by = ""
        self.energy_keV = None
        self.pixel_size_nm = None

    def read(self, filepath):
        logging.info("Reading parameters file: %s", filepath)

        lines = open(filepath, 'r').readlines()

        for line in lines:
            line = line.replace('(', '').replace(')', '')
            line = line.lower()

            keywords = self._get_keywords()
            value_formatters = self._get_value_formatter()
            for keyword in keywords:
                if keyword.lower() in line:
                    line = line.strip()
                    value = line.replace(keyword.lower(), '').replace("mlx::", '').replace(":", '')
                    value_formatter = value_formatters[keyword]
                    self._parameters[keyword] = value_formatter(value)

    def write(self, filepath):
        logging.info("Writing parameters file: %s", filepath)

        with open(filepath, 'w', newline='\n') as output_file:
            lines = []
            keywords = self._get_keywords()
            for keyword in keywords:
                line = "%12s \t %s\n" % (keyword, self._parameters[keyword])
                lines.append(line)

            output_file.writelines(lines)

    @staticmethod
    def _get_keywords():
        keywords = []

        keywords.append(KEY_WIDTH)
        keywords.append(KEY_HEIGHT)
        keywords.append(KEY_DEPTH)
        keywords.append(KEY_OFFSET)
        keywords.append(KEY_DATA_LENGTH_B)
        keywords.append(KEY_DATA_TYPE)
        keywords.append(KEY_BYTE_ORDER)
        keywords.append(KEY_RECORD_BY)
        keywords.append(KEY_ENERGY_keV)
        keywords.append(KEY_PIXEL_SIZE_nm)

        return keywords

    def _get_value_formatter(self):
        value_formatters = {}

        value_formatters[KEY_WIDTH] = int
        value_formatters[KEY_HEIGHT] = int
        value_formatters[KEY_DEPTH] = int
        value_formatters[KEY_OFFSET] = int
        value_formatters[KEY_DATA_LENGTH_B] = int
        value_formatters[KEY_DATA_TYPE] = self._extract_data_type
        value_formatters[KEY_BYTE_ORDER] = self._extract_byte_order
        value_formatters[KEY_RECORD_BY] = self._extract_record_by
        value_formatters[KEY_ENERGY_keV] = float
        value_formatters[KEY_PIXEL_SIZE_nm] = float

        return value_formatters

    @staticmethod
    def _extract_data_type(value_str):
        value_str = value_str.strip().lower()

        if value_str == DATA_TYPE_UNSIGNED:
            return DATA_TYPE_UNSIGNED
        elif value_str == DATA_TYPE_SIGNED:
            return DATA_TYPE_SIGNED

    @staticmethod
    def _extract_byte_order(value_str):
        value_str = value_str.strip().lower()

        if value_str == BYTE_ORDER_DONT_CARE:
            return BYTE_ORDER_DONT_CARE
        elif value_str == BYTE_ORDER_LITTLE_ENDIAN:
            return BYTE_ORDER_LITTLE_ENDIAN

    @staticmethod
    def _extract_string(value_str):
        return value_str.strip()

    @staticmethod
    def _extract_record_by(value_str):
        if RECORDED_BY_IMAGE in value_str:
            return RECORDED_BY_IMAGE
        elif RECORDED_BY_VECTOR in value_str:
            return RECORDED_BY_VECTOR

    @property
    def width(self):
        return self._parameters[KEY_WIDTH]

    @width.setter
    def width(self, width):
        self._parameters[KEY_WIDTH] = width

    @property
    def height(self):
        return self._parameters[KEY_HEIGHT]

    @height.setter
    def height(self, height):
        self._parameters[KEY_HEIGHT] = height

    @property
    def depth(self):
        return self._parameters[KEY_DEPTH]

    @depth.setter
    def depth(self, depth):
        self._parameters[KEY_DEPTH] = depth

    @property
    def offset(self):
        return self._parameters[KEY_OFFSET]

    @offset.setter
    def offset(self, offset):
        self._parameters[KEY_OFFSET] = offset

    @property
    def data_length_B(self):
        return self._parameters[KEY_DATA_LENGTH_B]

    @data_length_B.setter
    def data_length_B(self, data_length_B):
        self._parameters[KEY_DATA_LENGTH_B] = data_length_B

    @property
    def data_type(self):
        return self._parameters[KEY_DATA_TYPE]

    @data_type.setter
    def data_type(self, data_type):
        self._parameters[KEY_DATA_TYPE] = data_type

    @property
    def byte_order(self):
        return self._parameters[KEY_BYTE_ORDER]

    @byte_order.setter
    def byte_order(self, byte_order):
        self._parameters[KEY_BYTE_ORDER] = byte_order

    @property
    def record_by(self):
        return self._parameters[KEY_RECORD_BY]

    @record_by.setter
    def record_by(self, record_by):
        self._parameters[KEY_RECORD_BY] = record_by

    @property
    def energy_keV(self):
        return self._parameters[KEY_ENERGY_keV]

    @energy_keV.setter
    def energy_keV(self, energy_keV):
        self._parameters[KEY_ENERGY_keV] = energy_keV

    @property
    def pixel_size_nm(self):
        return self._parameters[KEY_PIXEL_SIZE_nm]

    @pixel_size_nm.setter
    def pixel_size_nm(self, pixel_size_nm):
        self._parameters[KEY_PIXEL_SIZE_nm] = pixel_size_nm

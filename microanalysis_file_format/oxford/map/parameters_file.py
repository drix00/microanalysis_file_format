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
DATA_TYPE_UNSIGNED = "UNSIGNED"
DATA_TYPE_SIGNED = "SIGNED"

BYTE_ORDER_DONT_CARE = "DONT-CARE"
BYTE_ORDER_LITTLE_ENDIAN = "LITTLE-ENDIAN"

KEY_WIDTH = "MLX::WIDTH"
KEY_HEIGHT = "MLX::HEIGHT"
KEY_DEPTH = "MLX::DEPTH"
KEY_OFFSET = "MLX::OFFSET"
KEY_DATA_LENGTH_B = "MLX::DATA-LENGTH"
KEY_DATA_TYPE = "MLX::DATA-TYPE :"
KEY_BYTE_ORDER = "MLX::BYTE-ORDER :"
KEY_RECORDED_BY = "MLX::RECORD-BY :"


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

    def read(self, filepath):
        logging.info("Reading parameters file: %s", filepath)

        lines = open(filepath, 'r').readlines()

        for line in lines:
            line = line.replace('(', '').replace(')', '')

            keywords = self._get_keywords()
            value_formatters = self._get_value_formatter()
            for keyword in keywords:
                if keyword in line:
                    value = line.replace(keyword, '')
                    value_formatter = value_formatters[keyword]
                    self._parameters[keyword] = value_formatter(value)

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
        keywords.append(KEY_RECORDED_BY)

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
        value_formatters[KEY_RECORDED_BY] = self._extract_string

        return value_formatters

    @staticmethod
    def _extract_data_type(value_str):
        value_str = value_str.strip().upper()

        if value_str == DATA_TYPE_UNSIGNED:
            return DATA_TYPE_UNSIGNED
        elif value_str == DATA_TYPE_SIGNED:
            return DATA_TYPE_SIGNED

    @staticmethod
    def _extract_byte_order(value_str):
        value_str = value_str.strip().upper()

        if value_str == BYTE_ORDER_DONT_CARE:
            return BYTE_ORDER_DONT_CARE
        elif value_str == BYTE_ORDER_LITTLE_ENDIAN:
            return BYTE_ORDER_LITTLE_ENDIAN

    @staticmethod
    def _extract_string(value_str):
        return value_str.strip()

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
        return self._parameters[KEY_RECORDED_BY]

    @record_by.setter
    def record_by(self, record_by):
        self._parameters[KEY_RECORDED_BY] = record_by

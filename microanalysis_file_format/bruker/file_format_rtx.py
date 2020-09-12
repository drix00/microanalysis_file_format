#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.bruker.file_format_rtx
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read EDS Esprit file format rtx.
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
import zlib
import base64
import logging
from xml.etree.ElementTree import ElementTree, XML

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.
TAG_HEADER = "RTHeader"
TAG_DATA = "RTData"
TAG_PROJECT_HEADER = "ProjectHeader"
TAG_COMPRESSION = "RTCompression"
TAG_DATE = "Date"
TAG_TIME = "Time"
TAG_CREATOR = "Creator"
TAG_COMMENT = "Comment"


class FileFormatRtx(object):
    def __init__(self):
        self._etree = ElementTree()

    def read_file(self, filepath):
        self._etree = ElementTree(file=filepath)

        logging.info("Root: %s", self._etree.getroot())

        root = self._etree.getroot()

        # for element in etree.getiterator():
        for element in root.getchildren():
            logging.debug("tag: %s", element.tag)
            logging.debug("    %s", element.text)
            # logging.debug("    %s", element.tail)
            logging.debug("    %s", element.attrib)

    def print_header(self):
        header_elements = self.get_header_elements()

        for element in header_elements:
            self._print_element(element)

    def get_header_elements(self):
        parent_element = self._etree.find(TAG_HEADER)
        elements = parent_element.getchildren()

        return elements

    def print_project_header(self):
        elements = self.get_project_header_elements()

        for element in elements:
            self._print_element(element)

    def get_project_header_elements(self):
        parent_element = self._etree.find("*//"+TAG_PROJECT_HEADER)
        elements = parent_element.getchildren()

        return elements

    def print_compression(self):
        element = self.get_compression_element()

        self._print_element(element)

    def get_compression_element(self):
        parent_element = self._etree.find("*//"+TAG_COMPRESSION)

        return parent_element

    def print_date(self):
        element = self.get_date_element()

        self._print_element(element)

    def get_date_element(self):
        parent_element = self._etree.find("*//"+TAG_DATE)

        return parent_element

    def print_time(self):
        element = self.get_time_element()

        self._print_element(element)

    def get_time_element(self):
        parent_element = self._etree.find("*//"+TAG_TIME)

        return parent_element

    def print_creator(self):
        element = self.get_creator_element()

        self._print_element(element)

    def get_creator_element(self):
        parent_element = self._etree.find("*//"+TAG_CREATOR)

        return parent_element

    def print_comment(self):
        element = self.get_comment_element()

        self._print_element(element)

    def get_comment_element(self):
        parent_element = self._etree.find("*//"+TAG_COMMENT)

        return parent_element

    @staticmethod
    def decompress(compressed_data):
        compressed_data = base64.b64decode(compressed_data)
        data = zlib.decompress(compressed_data)

        return data

    @staticmethod
    def extract_data(data):
        etree = XML(data)

        logging.info("Root: %s", etree.getroot())

    @staticmethod
    def _print_element(element):
        logging.info("tag: %s", element.tag)
        logging.info("    %s", element.text)
        # logging.info("    %s", element.tail)
        logging.info("    %s", element.attrib)

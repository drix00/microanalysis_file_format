#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: rtx_bruker

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Example how to read RTX file from Bruker.
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

# Third party modules.

# Local modules.

# Project modules.
from microanalysis_file_format.bruker.file_format_rtx import FileFormatRtx

# Globals and constants variables.


def run_data():
    import os.path

    path = r"../testData/bruker"
    filename = "CN.zlib"
    compressed_data_filepath = os.path.join(path, filename)

    compressed_data = open(compressed_data_filepath, 'rb').readlines()[0]

    file_format_rtx = FileFormatRtx()

    data = file_format_rtx.decompress(compressed_data)
    file_format_rtx.extract_data(data)

    print(data)

    path = r"../testData/bruker"
    filename = "CN.dat"
    decompressed_data_filepath = os.path.join(path, filename)

    decompressed_data_file = open(decompressed_data_filepath, 'wb')
    decompressed_data_file.write(data)


def run_rtx():
    import os.path

    path = r"../testData/bruker"
    filename = "CN.rtx"
    filepath = os.path.join(path, filename)
    file_format_rtx = FileFormatRtx()

    file_format_rtx.read_file(filepath)

    # file_format_rtx.print_header()
    # file_format_rtx.print_project_header()
    file_format_rtx.print_compression()
    file_format_rtx.print_date()
    file_format_rtx.print_time()
    file_format_rtx.print_creator()
    file_format_rtx.print_comment()

    # path = r"../testData/bruker"
    # filename = "CN.dat"
    # decompressedDataFilepath = os.path.join(path, filename)

    # decompressedDataFile = open(decompressedDataFilepath, 'wb')
    # decompressedDataFile.write(data)


def main():
    run_rtx()
    run_data()


if __name__ == '__main__':  # pragma: no cover
    main()
